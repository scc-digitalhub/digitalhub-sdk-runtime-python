# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from pathlib import Path

from pip._internal.operations import freeze

from digitalhub_runtime_python.entities._commons.requirement_parser.factory import RequirementParserFactory


class RequirementParser:
    """
    A utility class for parsing requirements files using pip's internal parser.
    """

    def parse(self, requirements: list[str] | str | None = None) -> list[str] | None:
        """
        Parse the requirements file.

        Returns
        -------
        list[str] | None
            A list of requirement strings or None if no requirements are provided.
        """
        if requirements is None:
            return
        elif isinstance(requirements, str):
            self._validate_path(requirements)
            parser = RequirementParserFactory().get_parser(requirements)
            parsed = parser.parse_requirements(requirements)
            return self.read_installed_packages(parsed)
        return self.read_installed_packages(requirements)

    def _validate_path(self, path: str) -> None:
        """
        Validate the provided path.
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Requirements file not found: {path}")
        if not Path(path).is_file():
            raise ValueError(f"Provided path is not a file: {path}")

    @staticmethod
    def read_installed_packages(requirements: list[str] | None = None) -> list[str] | None:
        """
        Read installed packages in execution context.

        If requirements is provided, returns only those packages with their
        versions filled in from the environment. Package names without versions
        in the requirements list will have their versions added if found.

        Parameters
        ----------
        requirements : list[str]
            Optional list of package names (e.g., ['pandas', 'torch']) or
            requirements with versions (e.g., ['pandas==2.0.0']).

        Returns
        -------
        list[str]
            List of installed packages in pip freeze format (e.g., ['numpy==1.24.0', 'pandas==2.0.0']).
        """
        separators = ["==", ">=", "<=", ">", "<", "~=", "!="]

        # Build a mapping of normalized package names to their installed versions
        installed_map: dict[str, str] = {}
        for pkg in freeze.freeze():
            # Handle different separators
            for sep in separators:
                if sep in pkg:
                    name, version = pkg.split(sep, 1)
                    # Normalize package name (lowercase, replace _ with -)
                    installed_map[name.lower().replace("_", "-")] = f"{name}{sep}{version}"
                    break

        result = []
        for req in requirements:
            # Check if requirement already has a version specifier
            has_version = any(sep in req for sep in separators)

            if has_version:
                # Keep as-is if version is already specified
                result.append(req)
            else:
                # Normalize the requirement name for lookup
                normalized_name = req.lower().replace("_", "-")
                if normalized_name in installed_map:
                    # Use the installed version
                    result.append(installed_map[normalized_name])
                else:
                    # Package not found in environment, keep without version
                    result.append(req)

        return result
