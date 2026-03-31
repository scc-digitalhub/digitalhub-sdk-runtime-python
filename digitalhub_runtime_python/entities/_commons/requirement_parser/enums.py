# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from enum import Enum


class RequirementFormat(Enum):
    """
    Enum for requirement file formats.
    """

    PIP = "pip"
    PYPROJECT = "pyproject"
    CONDA = "conda"


class RequirementFile(Enum):
    """
    Enum for requirement file names.
    """

    REQUIREMENTS_TXT = "requirements.txt"
    SETUP_PY = "setup.py"
    PYPROJECT_TOML = "pyproject.toml"
    CONDA_ENV_YAML = "conda.yaml"
    CONDA_ENV_YML = "conda.yml"
