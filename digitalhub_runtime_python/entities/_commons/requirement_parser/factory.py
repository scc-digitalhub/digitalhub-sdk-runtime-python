# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from pathlib import Path

from digitalhub_runtime_python.entities._commons.requirement_parser.enums import RequirementFile, RequirementFormat
from digitalhub_runtime_python.entities._commons.requirement_parser.modules._base import BaseParser
from digitalhub_runtime_python.entities._commons.requirement_parser.modules._conda import CondaParser
from digitalhub_runtime_python.entities._commons.requirement_parser.modules._pip import PipParser
from digitalhub_runtime_python.entities._commons.requirement_parser.modules._pyproject import PyProjectParser


class RequirementParserFactory:
    """
    Factory for requirement parsers.
    """

    def get_parser(self, requirements_file: str) -> BaseParser:
        """
        Get the requirement parser based on the format.

        Parameters
        ----------
        requirements_file : str
            The path to the requirements file.

        Returns
        -------
        BaseParser
            The requirement parser.
        """
        req_type = self._requirements_format(requirements_file)
        match req_type:
            case RequirementFormat.PIP:
                return PipParser()
            case RequirementFormat.PYPROJECT:
                return PyProjectParser()
            case RequirementFormat.CONDA:
                return CondaParser()
            case _:
                raise ValueError(f"No parser found for format: {requirements_file}")

    @staticmethod
    def _requirements_format(requirements_file: str) -> RequirementFormat:
        """
        Understand requirements file format.

        Parameters
        ----------
        requirements_file : str
            The path to the requirements file.

        Returns
        -------
        RequirementFormat
            The format of the requirements file (e.g., 'pip', 'pyproject', 'conda').
        """
        match Path(requirements_file).name:
            case RequirementFile.REQUIREMENTS_TXT.value:
                return RequirementFormat.PIP
            case RequirementFile.SETUP_PY.value:
                return RequirementFormat.PIP
            case RequirementFile.PYPROJECT_TOML.value:
                return RequirementFormat.PYPROJECT
            case RequirementFile.CONDA_ENV_YML.value:
                return RequirementFormat.CONDA
            case RequirementFile.CONDA_ENV_YAML.value:
                return RequirementFormat.CONDA
            case _:
                raise ValueError(
                    f"Unsupported requirements file: {Path(requirements_file).name}."
                    f" Supported filenames are: {', '.join([f.value for f in RequirementFile])}."
                )
