# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities.run._base.spec import RunSpecPython


class RunSpecPythonRunJob(RunSpecPython):
    """RunSpecPythonRunJob specifications."""

    local_execution: bool = False
    """Whether to execute the run locally instead of in the cluster."""
