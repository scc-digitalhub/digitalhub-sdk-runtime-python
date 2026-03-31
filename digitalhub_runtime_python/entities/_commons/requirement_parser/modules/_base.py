# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod


class BaseParser:
    @staticmethod
    @abstractmethod
    def parse_requirements(source: str) -> list[str]:
        """
        Parses the requirements file and returns a list of dependencies.
        """
