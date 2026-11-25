# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.function._base.entity import FunctionBaseFunction

if typing.TYPE_CHECKING:
    from digitalhub.plugins import Status

    from digitalhub_runtime_python.entities.function.openinference.spec import FunctionSpecOpeninference


class FunctionOpeninference(FunctionBaseFunction):
    """
    FunctionOpeninference class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: FunctionSpecOpeninference
        self.status: Status
