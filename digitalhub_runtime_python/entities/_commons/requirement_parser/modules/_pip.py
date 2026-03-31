# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements as pip_parse

from digitalhub_runtime_python.entities._commons.requirement_parser.modules._base import BaseParser


class PipParser(BaseParser):
    @staticmethod
    def parse_requirements(source: str) -> list[str]:
        """
        Parse a requirements.txt file using pip's internal parser.

        Parameters
        ----------
        source : str
            Path to a requirements.txt file.

        Returns
        -------
        list[str]
            A list of requirement strings as they would be understood by pip.

        Examples
        --------
        >>> requirements = parse_requirements_with_pip("/path/to/requirements.txt")
        >>> print(requirements)
        ['numpy>=1.0', 'pandas==2.0.0', 'git+https://github.com/user/repo.git@main']
        """
        # Parse using pip's internal parser
        session = PipSession()
        parsed = pip_parse(source, session=session)

        # Extract requirement strings
        requirements = []
        for req in parsed:
            if req.requirement:
                requirements.append(str(req.requirement))

        return requirements
