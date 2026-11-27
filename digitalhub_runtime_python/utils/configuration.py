# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from digitalhub.plugins import fetch_source
from digitalhub.utils.generic_utils import decode_base64_string, import_function
from digitalhub.utils.logger.logger import get_logger
from digitalhub.utils.uri_utils import has_local_scheme

logger = get_logger(__file__)
DEFAULT_PY_FILE = "main.py"
DEFAULT_SERVERLESS_PATH = Path("/shared")


def _parse_handler(handler: str) -> tuple[Path, str]:
    """
    Parse handler string into path and function name.

    Parameters
    ----------
    handler : str
        Function handler in format 'module:function' or 'path.to.module:function'.

    Returns
    -------
    tuple[Path, str]
        Handler path and function name.
    """
    parsed = handler.split(":")
    if len(parsed) == 1:
        return Path(""), parsed[0]
    return Path(*parsed[0].split(".")), parsed[1]


def _get_function_path(source_path: Path, handler: str) -> tuple[Path, str]:
    """
    Get function path and name from handler.

    Parameters
    ----------
    source_path : Path
        Root path where the function source is located.
    handler : str
        Function handler.

    Returns
    -------
    tuple[Path, str]
        Function path and function name.
    """
    handler_path, function_name = _parse_handler(handler)
    if handler_path == Path(""):
        handler_path = Path(DEFAULT_PY_FILE)
    function_path = (source_path / handler_path).with_suffix(".py")
    return function_path, function_name


def _import_function_from_path(function_path: Path, function_name: str) -> Callable:
    """
    Import a function from a file path.

    Parameters
    ----------
    function_path : Path
        Path to the Python file.
    function_name : str
        Name of the function to import.

    Returns
    -------
    Callable
        Imported function.
    """
    return import_function(function_path, function_name)


def import_function_from_source(path: Path, source_spec: dict, skip_save: bool = False) -> Callable:
    """
    Get function from source.

    Parameters
    ----------
    path : Path
        Path where to save the function source.
    source_spec : dict
        Function source spec.

    Returns
    -------
    Callable
        Function.
    """
    try:
        source_path = save_function_source(path, source_spec) if not skip_save else path
        function_path, function_name = _get_function_path(source_path, source_spec["handler"])
        return _import_function_from_path(function_path, function_name)
    except Exception as e:
        msg = f"Some error occurred while getting function. Exception: {e.__class__}. Error: {e.args}"
        logger.exception(msg)
        raise RuntimeError(msg) from e


def save_function_source(path: Path, source_spec: dict) -> Path:
    """
    Save function source from various sources.

    Parameters
    ----------
    path : Path
        Path where to save the function source.
    source_spec : dict
        Function source spec.

    Returns
    -------
    Path
        Path to the function source directory.
    """
    base64 = source_spec.get("base64")
    source = source_spec.get("source")

    # Base64-encoded source
    if base64 is not None:
        path.mkdir(parents=True, exist_ok=True)
        (path / DEFAULT_PY_FILE).write_text(decode_base64_string(base64))
        return path

    if source is None:
        raise RuntimeError("Function source not found in spec.")

    fetch_source(path, source)
    return path


def _get_function_to_import(handler: str, source_code: str | None, root_path: Path) -> tuple[Path, str]:
    """
    Get function name from handler string.

    Parameters
    ----------
    handler : str
        Function handler in format 'module:function' or 'path.to.module:function'.
    source_code : str | None
        Source code (used to infer function name if handler is just a function name).

    Returns
    -------
    tuple[Path, str]
        Function path and function name.
    """
    # If handler is not specified, assume function module is in main
    try:
        function_module, function_name = handler.split(":")
    except ValueError:
        function_name = handler
        if source_code is not None and has_local_scheme(source_code):
            function_module = ".".join(Path(source_code.removesuffix(".py")).parts)
        else:
            function_module = DEFAULT_PY_FILE.removesuffix(".py")

    function_path = (root_path / Path(function_module.replace(".", "/") + ".py")).resolve()
    if not function_path.exists():
        raise RuntimeError(f"Function module {function_module} not found at path {function_path}.")

    return function_path, function_name


def import_function_and_init_from_source(
    source_spec: dict,
    root_path: Path | None = None,
) -> tuple[Callable, Callable | None]:
    """
    Import main function and optional init function from source.

    Parameters
    ----------
    source_spec : dict
        Function source spec.
    root_path : Path | None
        Root path to use if function path is not specified.

    Returns
    -------
    tuple
        Main function and optional init function.
    """
    if root_path is None:
        root_path = DEFAULT_SERVERLESS_PATH

    handler = source_spec.get("handler")
    source_code = source_spec.get("source")

    function_path, function_name = _get_function_to_import(handler, source_code, root_path)

    # Import module and get main function
    main_function = _import_function_from_path(function_path, function_name)

    # Import init function if specified
    init_function: Callable | None = None
    init_handler: str | None = source_spec.get("init_function")
    if init_handler is not None:
        init_function = _import_function_from_path(function_path, init_handler)

    return main_function, init_function
