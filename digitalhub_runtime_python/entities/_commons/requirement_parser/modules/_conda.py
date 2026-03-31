# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

import yaml

from digitalhub_runtime_python.entities._commons.requirement_parser.modules._base import BaseParser


class CondaParser(BaseParser):
    @staticmethod
    def parse_requirements(source: str) -> list[str]:
        """
        Parse an environment.yml file.

        Parameters
        ----------
        source : str
            Path to an environment.yml file.

        Returns
        -------
        list[str]
            A list of requirement strings.
        """
        requirements = []

        with open(source, "r") as f:
            data = yaml.safe_load(f)

        if not data or "dependencies" not in data:
            return requirements

        for dep in data["dependencies"]:
            if isinstance(dep, dict) and "pip" in dep:
                requirements.extend(dep["pip"])

        return requirements
