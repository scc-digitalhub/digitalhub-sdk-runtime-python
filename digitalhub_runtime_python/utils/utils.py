# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
from typing import Callable

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements as pip_parse

from digitalhub_runtime_python.utils.outputs import collect_outputs


def handler(outputs: list[str] | None = None) -> Callable:
    """
    Decorator that handles the outputs of the function.

    Parameters
    ----------
    outputs : list[str]
        List of named outputs to collect.

    Returns
    -------
    Callable
        Decorated function.
    """
    if outputs is None:
        outputs = []

    def decorator(func: Callable) -> Callable:
        """
        Decorator that handles the outputs of the function.

        Parameters
        ----------
        func : Callable
            Function to decorate.

        Returns
        -------
        Callable
            Decorated function.
        """

        def wrapper(*args, **kwargs) -> dict:
            """
            Wrapper that handles the outputs of the function.

            Parameters
            ----------
            args : tuple
                Function arguments.
            kwargs : dict
                Function keyword arguments.

            Returns
            -------
            Any
                Function outputs.
            """
            # Initialize outputs
            nonlocal outputs

            # We pass the first argument as the project name
            # and the second argument as the run key
            project_name = args[0]
            run_key = args[1]
            args = args[2:]

            # Execute the function
            results = func(*args, **kwargs)

            # Parse outputs based on the decorator signature
            return collect_outputs(results, outputs, project_name, run_key)

        wrapper = functools.wraps(func)(wrapper)

        return wrapper

    return decorator


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
