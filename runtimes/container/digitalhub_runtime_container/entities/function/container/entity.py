from __future__ import annotations

import typing

from digitalhub.entities.function._base.entity import Function
from digitalhub.utils.generic_utils import decode_string
from digitalhub.utils.io_utils import write_text
from digitalhub.utils.uri_utils import map_uri_scheme

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.function.container.spec import FunctionSpecContainer
    from digitalhub_runtime_container.entities.function.container.status import FunctionStatusContainer

    from digitalhub.entities._base.entity.metadata import Metadata


class FunctionContainer(Function):
    """
    FunctionContainer class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecContainer,
        status: FunctionStatusContainer,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecContainer
        self.status: FunctionStatusContainer

    def export(self) -> str:
        """
        Export object as a YAML file in the context folder.

        Returns
        -------
        str
            Exported filepath.
        """
        # Strip base64 from source at following conditions:
        # - source is local path
        # - base64 is not None

        # Check source
        source = self.spec.source.get("source")
        if source is not None and map_uri_scheme(source) == "local":
            # Check base64. If it is set, decode it in a local file
            # save in variable to restore on object after export
            base64 = self.spec.source.pop("base64", None)
            if base64 is not None:
                # Write local file
                src_pth = self._context().root / source
                write_text(src_pth, decode_string(base64))

                # Export and restore base64, then return
                pth = super().export()
                self.spec.source["base64"] = base64
                return pth

        return super().export()
