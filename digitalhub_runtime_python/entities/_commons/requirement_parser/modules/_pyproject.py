# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from digitalhub_runtime_python.entities._commons.requirement_parser.modules._base import BaseParser


class PyProjectParser(BaseParser):
    @staticmethod
    def parse_requirements(source: str) -> list[str]:
        """
        Parse a pyproject.toml file.

        Parameters
        ----------
        source : str
            Path to a pyproject.toml file.

        Returns
        -------
        list[str]
            A list of requirement strings.
        """
        requirements = []

        with open(source, "rb") as f:
            data = tomllib.load(f)

        project = data.get("project", {})

        # Dependencies
        dependencies = project.get("dependencies", [])
        if isinstance(dependencies, list):
            requirements.extend(dependencies)

        return requirements
