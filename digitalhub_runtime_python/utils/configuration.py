# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
from typing import Callable, Union

from digitalhub.stores.data.api import get_store
from digitalhub.utils.generic_utils import (
    decode_base64_string,
    extract_archive,
    import_function,
    requests_chunk_download,
)
from digitalhub.utils.git_utils import clone_repository
from digitalhub.utils.logger import LOGGER
from digitalhub.utils.uri_utils import (
    get_filename_from_uri,
    has_git_scheme,
    has_local_scheme,
    has_remote_scheme,
    has_s3_scheme,
    has_zip_scheme,
)

DEFAULT_PY_FILE = "main.py"


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


def _download_and_extract_archive(source: str, path: Path) -> None:
    """
    Download and extract an archive from a URL or S3.

    Parameters
    ----------
    source : str
        Source URL (with zip+ scheme).
    path : Path
        Destination path.
    """
    clean_source = source.removeprefix("zip+")
    filename = path / get_filename_from_uri(source)

    if has_s3_scheme(clean_source):
        store = get_store(clean_source)
        store.get_s3_source(source, filename)
    else:
        requests_chunk_download(clean_source, filename)

    extract_archive(path, filename)
    filename.unlink()


def _save_base64_source(path: Path, base64_content: str) -> Path:
    """
    Save base64-encoded source to file.

    Parameters
    ----------
    path : Path
        Destination directory.
    base64_content : str
        Base64-encoded source code.

    Returns
    -------
    Path
        Path to the saved file (directory/main.py).
    """
    path.mkdir(parents=True, exist_ok=True)
    file_path = path / DEFAULT_PY_FILE
    file_path.write_text(decode_base64_string(base64_content))
    return path


def _download_remote_source(path: Path, source: str) -> Path:
    """
    Download source from remote URL (http/https).

    Parameters
    ----------
    path : Path
        Destination directory.
    source : str
        Remote source URL.

    Returns
    -------
    Path
        Path to the destination directory.
    """
    path.mkdir(parents=True, exist_ok=True)

    if has_zip_scheme(source):
        _download_and_extract_archive(source, path)
    else:
        filename = path / get_filename_from_uri(source)
        requests_chunk_download(source, filename)

    return path


def _download_s3_source(path: Path, source: str) -> Path:
    """
    Download source from S3.

    Parameters
    ----------
    path : Path
        Destination directory.
    source : str
        S3 source URL (must be zip+s3:// scheme).

    Returns
    -------
    Path
        Path to the destination directory.
    """
    if not has_zip_scheme(source):
        raise RuntimeError("S3 source must be a zip file with scheme zip+s3://.")

    path.mkdir(parents=True, exist_ok=True)
    _download_and_extract_archive(source, path)
    return path


def _clone_git_source(path: Path, source: str) -> Path:
    """
    Clone git repository.

    Parameters
    ----------
    path : Path
        Destination directory.
    source : str
        Git repository URL.

    Returns
    -------
    Path
        Path to the destination directory.
    """
    path.mkdir(parents=True, exist_ok=True)
    clone_repository(path, source)
    return path


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


def import_function_from_source(path: Path, source_spec: dict) -> Callable:
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
        source_path = save_function_source(path, source_spec)
        function_path, function_name = _get_function_path(source_path, source_spec["handler"])
        return _import_function_from_path(function_path, function_name)
    except Exception as e:
        msg = f"Some error occurred while getting function. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
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
        return _save_base64_source(path, base64)

    if source is None:
        raise RuntimeError("Function source not found in spec.")

    # Git repository
    if has_git_scheme(source):
        return _clone_git_source(path, source)

    # Remote HTTP(S) source
    if has_remote_scheme(source):
        return _download_remote_source(path, source)

    # S3 source
    if has_s3_scheme(source):
        return _download_s3_source(path, source)

    # Unsupported scheme
    raise RuntimeError(f"Unable to collect source from: {source}")


def import_function_and_init_from_source(
    path: Path,
    source_spec: dict,
) -> tuple[Callable, Union[Callable, None]]:
    """
    Import main function and optional init function from source.

    Parameters
    ----------
    path : Path
        Root path where the function source is downloaded.
    source_spec : dict
        Function source spec.

    Returns
    -------
    tuple
        Main function and optional init function.
    """
    # Get function path and import main function
    function_path, handler_name = _get_function_path(path, source_spec.get("handler"))
    main_function = _import_function_from_path(function_path, handler_name)

    # Import init function if specified
    init_function: Callable | None = None
    init_handler: str | None = source_spec.get("init_function")
    if init_handler is not None:
        init_function = _import_function_from_path(function_path, init_handler)

    return main_function, init_function


def get_function_source(path: Path, source_spec: dict, default_py: str) -> Path:
    """
    Get path to function source file.

    Parameters
    ----------
    path : Path
        Path where the function source is or must be saved.
    source_spec : dict
        Function source spec.
    default_py : str
        Default python file name.

    Returns
    -------
    Path
        Path to function source file.
    """
    base64 = source_spec.get("base64")
    source = source_spec.get("source", default_py)
    handler = source_spec.get("handler")

    # For base64-encoded sources from local files
    if base64 is not None:
        if not has_local_scheme(source):
            raise RuntimeError("Base64 source must have a local file scheme.")
        handler_path, _ = _parse_handler(handler)
        return path / handler_path / Path(source)

    # For other sources, construct path from handler
    handler_path, _ = _parse_handler(handler)
    if handler_path == Path(""):
        raise RuntimeError("Must provide handler path in handler in form <root>.<dir>.<module>:<function_name>.")

    return path / handler_path.with_suffix(".py")
