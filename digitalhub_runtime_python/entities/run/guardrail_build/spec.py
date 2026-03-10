# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities.run._base.spec import RunSpecPythonRun, RunValidatorPythonRun


class RunSpecGuardrailRunBuild(RunSpecPythonRun):
    """RunSpecGuardrailRunBuild specifications."""


class RunValidatorGuardrailRunBuild(RunValidatorPythonRun):
    """RunValidatorGuardrailRunBuild validator."""
