# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.function._base.entity import FunctionBaseFunction

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.status import Status

    from digitalhub_runtime_python.entities.function.guardrail.spec import FunctionSpecGuardrail


class FunctionGuardrail(FunctionBaseFunction):
    """
    FunctionGuardrail class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: FunctionSpecGuardrail
        self.status: Status
