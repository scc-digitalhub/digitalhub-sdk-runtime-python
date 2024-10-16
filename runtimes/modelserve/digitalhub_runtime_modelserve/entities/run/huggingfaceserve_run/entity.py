from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.run.modelserve_run.entity import RunModelserveRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_modelserve.entities.run.huggingfaceserve_run.spec import RunSpecHuggingfaceserveRun
    from digitalhub_runtime_modelserve.entities.run.huggingfaceserve_run.status import RunStatusHuggingfaceserveRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunHuggingfaceserveRun(RunModelserveRun):
    """
    RunHuggingfaceserveRun class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecHuggingfaceserveRun,
        status: RunStatusHuggingfaceserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecHuggingfaceserveRun
        self.status: RunStatusHuggingfaceserveRun