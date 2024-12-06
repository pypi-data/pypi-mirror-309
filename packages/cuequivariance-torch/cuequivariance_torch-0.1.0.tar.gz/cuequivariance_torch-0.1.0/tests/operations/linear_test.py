# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy
import logging

import pytest
import torch

import cuequivariance as cue
import cuequivariance_torch as cuet

list_of_irreps = [
    cue.Irreps("SU2", "3x1/2 + 4x1"),
    cue.Irreps("SU2", "2x1/2 + 5x1 + 2x1/2"),
    cue.Irreps("SU2", "2x1/2 + 0x1 + 0x1/2 + 1 + 2"),
]


@pytest.mark.parametrize("irreps_in", list_of_irreps)
@pytest.mark.parametrize("irreps_out", list_of_irreps)
@pytest.mark.parametrize("layout", [cue.mul_ir, cue.ir_mul])
@pytest.mark.parametrize("shared_weights", [True, False])
def test_linear_fwd(
    irreps_in: cue.Irreps,
    irreps_out: cue.Irreps,
    layout: cue.IrrepsLayout,
    shared_weights: bool,
):
    linear = cuet.Linear(
        irreps_in,
        irreps_out,
        layout=layout,
        shared_weights=shared_weights,
        device="cuda",
        dtype=torch.float64,
    )
    x = torch.randn(10, irreps_in.dim, dtype=torch.float64).cuda()

    if shared_weights:
        y = linear(x)
        y_fx = linear(x, use_fallback=True)
    else:
        w = torch.randn(10, linear.weight_numel, dtype=torch.float64).cuda()
        y = linear(x, w)
        y_fx = linear(x, w, use_fallback=True)

    assert y.shape == (10, irreps_out.dim)

    torch.testing.assert_close(y, y_fx)


@pytest.mark.parametrize("irreps_in", list_of_irreps)
@pytest.mark.parametrize("irreps_out", list_of_irreps)
@pytest.mark.parametrize("layout", [cue.mul_ir, cue.ir_mul])
@pytest.mark.parametrize("shared_weights", [True, False])
def test_linear_bwd_bwd(
    irreps_in: cue.Irreps,
    irreps_out: cue.Irreps,
    layout: cue.IrrepsLayout,
    shared_weights: bool,
):
    linear = cuet.Linear(
        irreps_in,
        irreps_out,
        layout=layout,
        shared_weights=shared_weights,
        device="cuda",
        dtype=torch.float64,
    )

    outputs = dict()
    for use_fallback in [True, False]:
        # reset the seed to ensure the same initialization
        torch.manual_seed(0)

        x = torch.randn(
            10, irreps_in.dim, requires_grad=True, device="cuda", dtype=torch.float64
        )

        if shared_weights:
            y = linear(x, use_fallback=use_fallback)
        else:
            w = torch.randn(
                10, linear.weight_numel, requires_grad=True, dtype=torch.float64
            ).cuda()
            y = linear(x, w, use_fallback=use_fallback)

        (grad,) = torch.autograd.grad(
            y.pow(2).sum(),
            x,
            create_graph=True,
        )

        grad.pow(2).sum().backward()

        outputs[use_fallback] = x.grad.clone()

    torch.testing.assert_close(outputs[True], outputs[False])


def test_e3nn_compatibility():
    try:
        from e3nn import o3
    except ImportError:
        pytest.skip("e3nn is not installed")

    with pytest.warns(UserWarning):
        irreps = o3.Irreps("3x1o + 4x1e")
        cuet.Linear(irreps, irreps, layout=cue.mul_ir)

    with pytest.warns(UserWarning):
        cuet.Linear("3x0e + 5x1o", "3x0e + 2x1o", layout=cue.ir_mul)


def test_no_layout_warning():
    with pytest.warns(UserWarning):
        cuet.Linear(cue.Irreps("SU2", "1"), cue.Irreps("SU2", "1"))


@pytest.mark.parametrize("irreps_in", list_of_irreps)
@pytest.mark.parametrize("irreps_out", list_of_irreps)
@pytest.mark.parametrize("layout", [cue.mul_ir, cue.ir_mul])
@pytest.mark.parametrize("shared_weights", [True, False])
def test_linear_copy(
    irreps_in: cue.Irreps,
    irreps_out: cue.Irreps,
    layout: cue.IrrepsLayout,
    shared_weights: bool,
):
    linear = cuet.Linear(
        irreps_in,
        irreps_out,
        layout=layout,
        shared_weights=shared_weights,
    ).cuda()

    copy.deepcopy(linear)
