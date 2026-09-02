# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.entity import Function
from digitalhub.utils.generic_utils import decode_base64_string
from digitalhub.utils.io_utils import write_text

from digitalhub_runtime_python.entities._commons.enums import Actions
from digitalhub_runtime_python.entities._commons.requirement_parser.parser import RequirementParser
from digitalhub_runtime_python.entities._commons.utils import export_local_source


class FunctionBaseFunction(Function):
    """
    Base class for runtime Python functions.
    """

    def _post_create_hook_before_save(self) -> None:
        """
        Parse function requirements before saving the entity.

        Returns
        -------
        None
            This method updates the function requirements in place.
        """
        self.spec.requirements = RequirementParser().parse(self.spec.requirements)

    def export(self) -> str:
        """
        Export the function to the context folder.

        Returns
        -------
        str
            Exported filepath.
        """
        with export_local_source(self.spec.source, self._context().root):
            config = getattr(self.spec, "config", None)
            # Check base64. If it is set, decode it in a local file
            # save in variable to restore on object after export
            base64 = None
            if config is not None:
                base64 = config.pop("base64", None)
                if base64 is not None:
                    # Write local file
                    config_pth = self._context().root / "config.yaml"
                    write_text(config_pth, decode_base64_string(base64))

            try:
                return super().export()
            finally:
                if config is not None and base64 is not None:
                    config["base64"] = base64

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
        if auto_build and self.spec.image is None:
            self.build(wait=True, log_info=log_info)

        return super().run(
            action,
            wait=wait,
            log_info=log_info,
            extensions=extensions,
            **kwargs,
        )
