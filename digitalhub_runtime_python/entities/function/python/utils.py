# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.stores.data.api import get_default_store, get_store
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.file_utils import eval_py_type, eval_zip_type
from digitalhub.utils.generic_utils import encode_string, read_source
from digitalhub.utils.uri_utils import has_local_scheme
from pip._internal.operations import freeze

from digitalhub_runtime_python.entities.function.python.models import Lang

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function.python.entity import FunctionPython


SEPARATORS = ["==", ">=", "<=", ">", "<", "~=", "!="]


def source_check(**kwargs) -> dict:
    """
    Check source code.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    dict
        Checked source.
    """
    source: dict = kwargs.pop("source", None)
    code_src = kwargs.pop("code_src", None)
    code = kwargs.pop("code", None)
    base64 = kwargs.pop("base64", None)
    handler = kwargs.pop("handler", None)
    init_function = kwargs.pop("init_function", None)
    lang = kwargs.pop("lang", None)

    if source is not None:
        code_src = source.pop("source", None)
        code = source.pop("code", None)
        base64 = source.pop("base64", None)
        handler = source.pop("handler", None)
        init_function = source.pop("init_function", None)
        lang = source.pop("lang", None)

    kwargs["source"] = _check_params(
        code_src=code_src,
        code=code,
        base64=base64,
        handler=handler,
        init_function=init_function,
        lang=lang,
    )
    return kwargs


def _check_params(
    code_src: str | None = None,
    code: str | None = None,
    base64: str | None = None,
    handler: str | None = None,
    init_function: str | None = None,
    lang: str | None = None,
) -> dict:
    """
    Check source.

    Parameters
    ----------
    code_src : str
        Source code source.
    code : str
        Source code.
    base64 : str
        Source code base64.
    handler : str
        Function handler.
    init_function : str
        Init function.
    lang : str
        Source code language.

    Returns
    -------
    dict
        Checked source.
    """
    source = {}

    if handler is None:
        raise EntityError("Handler must be provided.")
    source["handler"] = handler

    if init_function is not None:
        source["init_function"] = init_function

    if lang is None:
        source["lang"] = Lang.PYTHON.value

    if code_src is None and code is None and base64 is None:
        raise EntityError("Source must be provided.")

    if code_src is not None:
        source["source"] = code_src

    if base64 is not None:
        source["base64"] = base64

    if code is not None:
        source["base64"] = encode_string(code)

    return source


def source_post_check(exec: FunctionPython) -> FunctionPython:
    """
    Post check source.

    Parameters
    ----------
    exec : FunctionPython
        Executable.

    Returns
    -------
    FunctionPython
        Updated executable.
    """
    code_src = exec.spec.source.get("source", None)
    base64 = exec.spec.source.get("base64", None)
    if code_src is None or base64 is not None:
        return exec

    # Check local source
    if has_local_scheme(code_src):
        if not Path(code_src).is_file():
            raise EntityError(f"Source file {code_src} does not exist.")

        # Check py
        if eval_py_type(code_src):
            exec.spec.source["base64"] = read_source(code_src)

        # Check zip
        elif eval_zip_type(code_src):
            filename = Path(code_src).name
            dst = f"zip+{get_default_store(exec.project)}/{exec.project}/{exec.ENTITY_TYPE}/{exec.name}/{exec.id}/{filename}"
            get_store(dst).upload(code_src, dst)
            exec.spec.source["source"] = dst
            if ":" not in exec.spec.source["handler"]:
                exec.spec.source["handler"] = f"{Path(code_src).stem}:{exec.spec.source['handler']}"

    return exec


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
    if requirements is None:
        return

    # Build a mapping of normalized package names to their installed versions
    installed_map: dict[str, str] = {}
    for pkg in freeze.freeze():
        # Handle different separators
        for sep in SEPARATORS:
            if sep in pkg:
                name, version = pkg.split(sep, 1)
                # Normalize package name (lowercase, replace _ with -)
                installed_map[name.lower().replace("_", "-")] = f"{name}{sep}{version}"
                break

    result = []
    for req in requirements:
        # Check if requirement already has a version specifier
        has_version = any(sep in req for sep in SEPARATORS)

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
