# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.function._base.entity import FunctionBaseFunction

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function.ray.spec import FunctionSpecRay
    from digitalhub_runtime_python.entities.function.ray.status import FunctionStatusRay


class FunctionRay(FunctionBaseFunction):
    """
    FunctionRay class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: FunctionSpecRay
        self.status: FunctionStatusRay
