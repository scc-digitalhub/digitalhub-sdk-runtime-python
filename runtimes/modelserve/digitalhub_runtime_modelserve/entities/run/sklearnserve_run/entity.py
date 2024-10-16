from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.run.modelserve_run.entity import RunModelserveRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_modelserve.entities.run.sklearnserve_run.spec import RunSpecSklearnserveRun
    from digitalhub_runtime_modelserve.entities.run.sklearnserve_run.status import RunStatusSklearnserveRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunSklearnserveRun(RunModelserveRun):
    """
    RunSklearnserveRun class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecSklearnserveRun,
        status: RunStatusSklearnserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecSklearnserveRun
        self.status: RunStatusSklearnserveRun