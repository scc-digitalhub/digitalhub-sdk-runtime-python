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
from digitalhub.utils.generic_utils import create_archive, encode_string, read_source
from digitalhub.utils.uri_utils import has_local_scheme

from digitalhub_runtime_python.entities.function.python.models import Lang

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function.python.entity import FunctionPython


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

    config = _check_params(
        config_src=config_src,
        config_content=config_content,
        config_base64=config_base64,
        path=config_path,
    )

    if config is not None:
        kwargs["config"] = config
        return kwargs

    return kwargs


def _check_params(
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
