# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.entities._commons.utils import build_zip_path
from digitalhub.stores.data.api import get_store
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.file_utils import eval_py_type, eval_zip_type
from digitalhub.utils.generic_utils import create_archive, decode_base64_string, encode_string, read_source
from digitalhub.utils.io_utils import write_text
from digitalhub.utils.uri_utils import has_local_scheme

from digitalhub_runtime_python.entities.function.python.models import Lang

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function.python.entity import FunctionPython


class _LocalSourceExport:
    def __init__(self, source: dict, root: Path) -> None:
        self.source = source
        self.root = root
        self.base64 = None

    def __enter__(self) -> None:
        # Strip base64 from source at following conditions:
        # - source is local path
        # - base64 is not None
        source_path = self.source.get("source")
        if source_path is None or not has_local_scheme(source_path):
            return

        # Check base64. If it is set, decode it in a local file
        # save in variable to restore on object after export
        self.base64 = self.source.pop("base64", None)
        if self.base64 is not None:
            # Write local file
            write_text(self.root / source_path, decode_base64_string(self.base64))
        return

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Restore base64 after export, including when export raises an exception.
        if self.base64 is not None:
            self.source["base64"] = self.base64


def export_local_source(source: dict, root: Path) -> _LocalSourceExport:
    return _LocalSourceExport(source, root)


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
        source = source.copy()
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

    source["lang"] = lang if lang is not None else Lang.PYTHON.value

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
        path_src = Path(code_src)

        if not path_src.exists():
            raise EntityError(f"Source {code_src} does not exist.")

        # If source is a folder, zip it and upload it
        if not path_src.is_file():
            archive_path = create_archive(path_src)
            try:
                dst = build_zip_path(exec, archive_path.name)
                get_store(dst).upload(str(archive_path), dst)
                exec.spec.source["source"] = dst
            finally:
                archive_path.unlink(missing_ok=True)

        # If source is a file, read it and encode it in base64
        elif eval_py_type(code_src):
            exec.spec.source["base64"] = read_source(code_src)

        # If source is a zip file, upload it and update the source
        elif eval_zip_type(code_src):
            dst = build_zip_path(exec, path_src.name)
            get_store(dst).upload(code_src, dst)
            exec.spec.source["source"] = dst

    return exec
