"""
KFP pipeline Function specification module.
"""
from __future__ import annotations

from pathlib import Path

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec, SourceCodeStruct
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string, encode_source, encode_string
from digitalhub_core.utils.uri_utils import map_uri_scheme


class FunctionSpecKFP(FunctionSpec):
    """
    Specification for a Function pipeline.
    """

    def __init__(
        self,
        source: str | None = None,
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        requirements: list | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        image : str
            Name of the Function's container image.
        tag : str
            Tag of the Function's container image.
        source : str
            Function source name.
        handler : str
            Function handler name.
        command : str
            Command to run inside the container.
        requirements : list
            List of requirements for the Function.
        """
        super().__init__()

        self.image = image
        self.tag = tag
        self.handler = handler
        self.command = command
        self.requirements = requirements if requirements is not None else []

        self._source_check(source)
        if "lang" not in source:
            source["lang"] = "python"
        self.source = SourceCodeStruct(**source)

    @staticmethod
    def _source_check(source: dict) -> dict:
        """
        Check source.

        Parameters
        ----------
        source : dict
            Source.

        Returns
        -------
        dict
            Checked source.
        """
        if source is None:
            raise EntityError("Source must be provided.")

        # Source check
        source_path = source.get("source")
        code = source.get("code")
        base64 = source.get("base64")

        if source.get("lang") is None:
            source["lang"] = "python"

        if source_path is None and code is None and base64 is None:
            raise EntityError("Source must be provided.")

        if base64 is not None:
            return source

        if code is not None:
            source["base64"] = encode_string(code)
            return source

        if (source_path is not None) and (map_uri_scheme(source_path) == "local"):
            if not (Path(source_path).suffix == ".py" and Path(source_path).is_file()):
                raise EntityError("Source is not a valid python file.")
            source["base64"] = encode_source(source_path)

        return source

    def show_source_code(self) -> str:
        """
        Show source code.

        Returns
        -------
        str
            Source code.
        """
        if self.source.code is not None:
            return str(self.source.code)
        if self.source.base64 is not None:
            try:
                return decode_string(self.source.base64)
            except Exception:
                raise EntityError("Something got wrong during source code decoding.")
        if (self.source.source is not None) and (map_uri_scheme(self.source.source) == "local"):
            try:
                return Path(self.source.source).read_text()
            except Exception:
                raise EntityError("Cannot access source code.")
        return ""

    def to_dict(self) -> dict:
        """
        Override to_dict to exclude code from source.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        dict_["source"] = self.source.to_dict()
        return dict_


class FunctionParamsKFP(FunctionParams):
    """
    Function kfp parameters model.
    """

    source: dict
    "Source code"

    image: str = None
    """Name of the Function's container image."""

    tag: str = None
    """Tag of the Function's container image."""

    handler: str = None
    """Function handler name."""

    command: str = None
    """Command to run inside the container."""

    requirements: list = None
    """List of requirements for the Function."""
