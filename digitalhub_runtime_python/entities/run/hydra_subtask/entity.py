# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run.hydra_job.entity import RunHydraRunJob
if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.hydra_subtask.spec import RunSpecHydraRunSubtask
    from digitalhub_runtime_python.entities.run.hydra_subtask.status import RunStatusHydraRunSubtask

class RunHydraRunSubtask(RunHydraRunJob):
    """
    RunHydraRunSubtask class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecHydraRunSubtask
        self.status: RunStatusHydraRunSubtask