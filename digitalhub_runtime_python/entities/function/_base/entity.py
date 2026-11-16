# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from digitalhub.entities._mixin.source.entity import SourceEntityMixin
from digitalhub.entities.function._base.entity import Function
from digitalhub.utils.file_utils import eval_py_type
from digitalhub.utils.generic_utils import decode_base64_string
from digitalhub.utils.io_utils import write_text
from pydantic import BaseModel

from digitalhub_runtime_python.entities._commons.enums import Actions
from digitalhub_runtime_python.entities.function._base.utils import get_current_python_version

if TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec


class FunctionBaseFunction(SourceEntityMixin, Function):
    """
    Base class for runtime Python functions.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.spec: FunctionBaseSpec  # ty: ignore[incompatible-mutable-override]

    def _post_create_hook_before_save(self) -> None:
        """
        Parse function requirements before saving the entity.

        Returns
        -------
        None
            This method updates the function requirements in place.
        """
        from digitalhub_runtime_python.entities._commons.requirement_parser.parser import RequirementParser

        try:
            self.spec.python_version = self.spec.python_version or get_current_python_version()
        except AttributeError:
            pass
        self.spec.requirements = RequirementParser().parse(self.spec.requirements)

    def export(self) -> str:
        """
        Export the function to the context folder.

        Returns
        -------
        str
            Exported filepath.
        """
        config = getattr(self.spec, "config", None)
        if config is None:
            return super().export()

        if isinstance(config, BaseModel):
            if "base64" not in type(config).model_fields or (base64 := config.model_dump().get("base64")) is None:
                return super().export()
            self.spec.config = config.model_copy(update={"base64": None})
        else:
            if (base64 := config.get("base64")) is None:
                return super().export()
            export_config = dict(config)
            export_config.pop("base64")
            self.spec.config = export_config
        try:
            config_pth = self._context().root / "config.yaml"
            write_text(config_pth, decode_base64_string(base64))
            return super().export()
        finally:
            self.spec.config = config

    def _is_inlineable_source(self, path: str) -> bool:
        return eval_py_type(path)

    def build(
        self,
        wait: bool = True,
        log_info: bool = True,
        extensions: list[dict] | None = None,
        **kwargs,
    ):
        """
        Build the function using the build action.

        Parameters
        ----------
        wait : bool
            Whether to wait for the build to complete.
        log_info : bool
            Whether to log information while waiting.
        extensions : list[dict] | None
            List of extensions to apply.
        **kwargs : dict
            Keyword arguments passed to the run builder.

        Returns
        -------
        Run
            Build run instance.
        """
        return super().run(
            Actions.BUILD.value,
            wait=wait,
            log_info=log_info,
            extensions=extensions,
            **kwargs,
        )

    def run(
        self,
        action: str,
        wait: bool = False,
        log_info: bool = True,
        extensions: list[dict] | None = None,
        auto_build: bool = False,
        **kwargs,
    ):
        """
        Run the function, building it first when no image is available.

        Parameters
        ----------
        action : str
            Action to execute.
        wait : bool
            Whether to wait for execution to complete.
        log_info : bool
            Whether to log information while waiting.
        extensions : list[dict] | None
            List of extensions to apply.
        auto_build : bool
            Whether to build the function when ``spec.image`` is ``None``.
        **kwargs : dict
            Keyword arguments passed to the run builder.

        Returns
        -------
        Run
            Run instance.
        """
        if kwargs.get("local_execution", False):
            self._check_python_version()

        if auto_build and self.spec.image is None:
            self.build(wait=True, log_info=log_info)

        return super().run(
            action,
            wait=wait,
            log_info=log_info,
            extensions=extensions,
            **kwargs,
        )

    def _check_python_version(self) -> None:
        """Raise when a local run requests a different Python version."""
        python_version = self.spec.python_version
        current_python_version = get_current_python_version()
        if python_version is not None and python_version != current_python_version:
            raise ValueError(
                f"Local execution cannot use python_version='{python_version}'; "
                f"current Python version is {current_python_version}."
            )
