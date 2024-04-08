"""
General utilities module.
"""
from __future__ import annotations

import base64
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

import requests
from digitalhub_core.utils.io_utils import read_text
from git import Repo


def build_uuid(uuid: str | None = None) -> str:
    """
    Create a uuid if not given

    Parameters
    ----------
    uuid : str
        ID of the object in form of UUID. Optional.

    Returns
    -------
    str
        The uuid.
    """
    if uuid is not None:
        return uuid
    return str(uuid4())


def get_timestamp() -> str:
    """
    Get the current timestamp timezoned.

    Returns
    -------
    str
        The current timestamp.
    """
    return datetime.now().astimezone().isoformat()


def decode_string(string: str) -> str:
    """
    Decode a string from base64.

    Parameters
    ----------
    string : str
        The string to decode.

    Returns
    -------
    str
        The string decoded from base64.
    """
    return base64.b64decode(string).decode()


def encode_string(string: str) -> str:
    """
    Encode a string in base64.

    Parameters
    ----------
    string : str
        The string to encode.

    Returns
    -------
    str
        The string encoded in base64.
    """
    return base64.b64encode(string.encode()).decode()


def encode_source(path: str) -> str:
    """
    Read a file and encode in base64 the content.

    Parameters
    ----------
    path : str
        The file path to read.

    Returns
    -------
    str
        The file content encoded in base64.
    """
    return encode_string(read_text(path))


def set_dhub_env(
    endpoint: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
) -> None:
    """
    Function to set environment variables for DHub Core config.

    Parameters
    ----------
    endpoint : str
        The endpoint of DHub Core.
    user : str
        The user of DHub Core.
    password : str
        The password of DHub Core.
    token : str
        The token of DHub Core.

    Returns
    -------
    None
    """
    if endpoint is not None:
        os.environ["DIGITALHUB_CORE_ENDPOINT"] = endpoint
    if user is not None:
        os.environ["DIGITALHUB_CORE_USER"] = user
    if password is not None:
        os.environ["DIGITALHUB_CORE_PASSWORD"] = password
    if token is not None:
        os.environ["DIGITALHUB_CORE_TOKEN"] = token


def parse_entity_key(key: str) -> tuple[str]:
    """
    Parse the entity key.

    Parameters
    ----------
    key : str
        The entity key.

    Returns
    -------
    tuple[str]
        Project, entity type, kind, name and uuid.
    """
    try:
        # Remove "store://" from the key
        key = key.replace("store://", "")
        # Split the key into parts
        parts = key.split("/")
        # The project is the first part
        project = parts[0]
        # The entity type is the second part
        entity_type = parts[1]
        # The kind is the third part
        kind = parts[2]
        # The name and uuid are separated by a colon in the last part
        name, uuid = parts[3].split(":")
        return project, entity_type, kind, name, uuid
    except Exception as e:
        raise ValueError("Invalid key format.") from e


def clone_repository(path: Path, source: str) -> None:
    """
    Clone repository.

    Parameters
    ----------
    path : Path
        Path where to save the repository.
    source : str
        HTTP(S) URL of the repository.

    Returns
    -------
    None
    """
    Repo.clone_from(source, path)


def requests_chunk_download(source: str, filename: Path) -> None:
    """
    Download a file in chunks.

    Parameters
    ----------
    source : str
        URL to download the file.
    filename : Path
        Path where to save the file.

    Returns
    -------
    None
    """
    with requests.get(source, stream=True) as r:
        r.raise_for_status()
        with filename.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def extract_archive(path: Path, filename: Path) -> None:
    """
    Extract an archive.

    Parameters
    ----------
    path : Path
        Path where to extract the archive.
    filename : Path
        Path to the archive.

    Returns
    -------
    None
    """
    with ZipFile(filename, "r") as zip_file:
        zip_file.extractall(path)
