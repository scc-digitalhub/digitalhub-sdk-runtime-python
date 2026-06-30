# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.generic_utils import encode_string, read_source
from digitalhub.utils.uri_utils import has_local_scheme

from digitalhub_runtime_python.entities.function.python.models import Lang

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
    complete_function = kwargs.pop("complete_function", None)
    lang = kwargs.pop("lang", None)

    if source is not None:
        code_src = source.pop("source", None)
        code = source.pop("code", None)
        base64 = source.pop("base64", None)
        handler = source.pop("handler", None)
        init_function = source.pop("init_function", None)
        complete_function = source.pop("complete_function", None)
        lang = source.pop("lang", None)

    kwargs["source"] = _check_params(
        code_src=code_src,
        code=code,
        base64=base64,
        handler=handler,
        init_function=init_function,
        complete_function=complete_function,
        lang=lang,
    )
    return kwargs


def _check_params(
    code_src: str | None = None,
    code: str | None = None,
    base64: str | None = None,
    handler: str | None = None,
    init_function: str | None = None,
    complete_function: str | None = None,
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
    complete_function : str
        Complete function.
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

    if complete_function is not None:
        source["complete_function"] = complete_function

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



def config_check(**kwargs) -> dict:
    """
    Check config.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    dict
        Checked config.
    """
    # either config_src or config or config_base64 may be provided
    config_src = kwargs.pop("config_src", None)
    config_base64 = kwargs.pop("config_base64", None)
    config_content = kwargs.pop("config_content", None)
    config = kwargs.pop("config", None)
    config_path = kwargs.pop("config_path", None)

    if config is not None:
        config_src = config.pop("source", None)
        config_base64 = config.pop("base64", None)
        config_content = None
        config_path = config.pop("path", None)

    config = _check_config_params(
        config_src=config_src,
        config_content=config_content,
        config_base64=config_base64,
        path=config_path,
    )

    if config is not None:
        kwargs["config"] = config
        return kwargs

    return kwargs


def _check_config_params(
    config_src: str | None = None,
    config_content: str | None = None,
    config_base64: str | None = None,
    path: str | None = None,
) -> dict:
    """
    Check config.

    Parameters
    ----------
    config_src : str
        Config source.
    config_content : str
        Config.
    config_base64 : str
        Config base64.
    path : str
        Config path.

    Returns
    -------
    dict
        Checked config.
    """
    config = {}

    if path is not None:
        config["path"] = path

    if config_src is None and config_content is None and config_base64 is None:
        raise EntityError("Config must be provided.")

    if config_src is not None:
        # Check local source
        if has_local_scheme(config_src):
            path_src = Path(config_src)

            if not path_src.exists():
                raise EntityError(f"Source {config_src} does not exist.")

            # If source is a folder, zip it and upload it
            if not path_src.is_file():
                raise EntityError(f"Source {config_src} should be a file.")

            # If source is a file, read it and encode it in base64
            config["base64"] = read_source(config_src)
        else:
            config["source"] = config_src

    if config_base64 is not None:
        config["base64"] = config_base64

    if config_content is not None:
        config["base64"] = encode_string(config_content)

    return config
