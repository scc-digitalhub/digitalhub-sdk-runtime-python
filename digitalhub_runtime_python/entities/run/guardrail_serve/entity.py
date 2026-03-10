# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run._base.entity import RunPythonRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.guardrail_serve.spec import RunSpecGuardrailRunServe
    from digitalhub_runtime_python.entities.run.guardrail_serve.status import RunStatusGuardrailRunServe


class RunGuardrailRunServe(RunPythonRun):
    """
    RunGuardrailRunServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecGuardrailRunServe
        self.status: RunStatusGuardrailRunServe
