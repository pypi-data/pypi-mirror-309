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
import numpy as np
import pytest
import torch

import cuequivariance as cue
import cuequivariance_torch as cuet


@pytest.mark.parametrize(
    "dtype, tol",
    [(torch.float64, 1e-6), (torch.float32, 1e-4)],
)
@pytest.mark.parametrize("l", [1, 2, 3])
def test_spherical_harmonics(l: int, dtype, tol):
    vec = torch.randn(3, dtype=dtype)
    axis = np.random.randn(3)
    angle = np.random.rand()
    scale = 1.3

    yl = cuet.spherical_harmonics([l], vec, False)

    R = torch.from_numpy(cue.SO3(1).rotation(axis, angle)).to(dtype)
    Rl = torch.from_numpy(cue.SO3(l).rotation(axis, angle)).to(dtype)

    yl1 = cuet.spherical_harmonics([l], scale * R @ vec, False)
    yl2 = scale**l * Rl @ yl

    torch.testing.assert_close(yl1, yl2, rtol=tol, atol=tol)


def test_spherical_harmonics_full():
    vec = torch.randn(3)
    ls = [0, 1, 2, 3]
    yl = cuet.spherical_harmonics(ls, vec, False)

    assert abs(yl[0] - 1.0) < 1e-6
