# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.function.crud import new_function

from digitalhub_runtime_python.entities.function.python.builder import FunctionPythonBuilder

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function.python.entity import FunctionPython


def new_function_python(
    project: str,
    name: str,
    source: dict | None = None,
    code: str | None = None,
    code_src: str | None = None,
    handler: str | None = None,
    init_function: str | None = None,
    lang: str | None = None,
    image: str | None = None,
    base_image: str | None = None,
    python_version: str | None = None,
    requirements: list[str] | str | None = None,
    uuid: str | None = None,
    version: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = False,
) -> FunctionPython:
    """
    Create a Python function entity.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Function name.
    source : dict, optional
        Function source configuration.
    code : str, optional
        Function source code as plain text.
    code_src : str, optional
        Local path or URI pointing to the function source code.
    handler : str, optional
        Function entrypoint.
    init_function : str, optional
        Initialization function to run before the handler.
    lang : str, optional
        Source code language hint.
    image : str, optional
        Function container image.
    base_image : str, optional
        Base container image used to build the function image.
    python_version : str, optional
        Python version used by the function runtime.
    requirements : list[str] or str, optional
        Python dependencies required by the function.
    uuid : str, optional
        Function identifier.
    version : str, optional
        Function version.
    description : str, optional
        Human-readable function description.
    labels : list[str], optional
        Function labels.
    embedded : bool, default=False
        Whether to embed the function specification in the project specification.

    Returns
    -------
    FunctionPython
        Created Python function entity.
    """
    if code is not None and code_src is not None:
        raise ValueError("Only one of 'code' or 'code_src' can be provided.")

    return new_function(
        project=project,
        name=name,
        kind=FunctionPythonBuilder.ENTITY_KIND,
        uuid=uuid,
        version=version,
        description=description,
        labels=labels,
        embedded=embedded,
        source=source,
        code=code,
        code_src=code_src,
        handler=handler,
        init_function=init_function,
        lang=lang,
        image=image,
        base_image=base_image,
        python_version=python_version,
        requirements=requirements,
    )
