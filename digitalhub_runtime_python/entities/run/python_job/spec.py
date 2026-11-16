# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.spec import LocalExecutionSpecMixin

from digitalhub_runtime_python.entities.run._base.spec import RunSpecPython


class RunSpecPythonRunJob(RunSpecPython, LocalExecutionSpecMixin):
    """RunSpecPythonRunJob specifications."""
