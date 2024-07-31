from __future__ import annotations

import pickle
from typing import Any

from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifact.crud import log_artifact
from digitalhub_core.entities.artifact.entity._base import Artifact
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitem.crud import log_dataitem
from digitalhub_data.entities.dataitem.entity.table import DataitemTable
from digitalhub_data.readers.registry import DATAFRAME_TYPES


def collect_outputs(results: Any, outputs: list[str], project_name: str) -> dict:
    """
    Collect outputs. Use the produced results directly.

    Parameters
    ----------
    results : Any
        Function outputs.
    project : Project
        Project object.

    Returns
    -------
    dict
        Function outputs.
    """
    objects = {}
    results = listify_results(results)

    for idx, item in enumerate(results):
        try:
            name = outputs[idx]
        except IndexError:
            name = f"output_{idx}"

        if isinstance(item, (str, int, float, bool, bytes)):
            objects[name] = item

        elif f"{item.__class__.__module__}.{item.__class__.__name__}" in DATAFRAME_TYPES:
            objects[name] = _log_dataitem(name, project_name, item)

        else:
            objects[name] = _log_artifact(name, project_name, item)

    return objects


def parse_outputs(results: Any, run_outputs: list, project_name: str) -> dict:
    """
    Parse outputs.

    Parameters
    ----------
    results : Any
        Function outputs.
    project : Project
        Project object.

    Returns
    -------
    dict
        Function outputs.
    """
    results_list = listify_results(results)
    out_list = []
    for idx, _ in enumerate(results_list):
        try:
            out_list.append(run_outputs.pop(0))
        except IndexError:
            out_list.append(f"output_{idx}")
    return collect_outputs(results, out_list, project_name)


def listify_results(results: Any) -> list:
    """
    Listify results.

    Parameters
    ----------
    results : Any
        Function outputs.

    Returns
    -------
    list
        Function outputs.
    """
    if results is None:
        return []

    if not isinstance(results, (tuple, list)):
        results = [results]

    return results


def _log_dataitem(name: str, project_name: str, data: Any) -> DataitemTable:
    """
    Log dataitem.

    Parameters
    ----------
    name : str
        Dataitem name.
    project_name : str
        Project name.
    data : Any
        Dataframe.

    Returns
    -------
    str
        Dataitem key.
    """
    try:
        return log_dataitem(
            project=project_name,
            name=name,
            kind="table",
            data=data,
        )
    except Exception as e:
        msg = f"Some error occurred while logging dataitem. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def _log_artifact(name: str, project_name: str, data: Any) -> Artifact:
    """
    Log artifact.

    Parameters
    ----------
    name : str
        Artifact name.
    project_name : str
        Project name.
    data : Any
        Data.

    Returns
    -------
    str
        Artifact key.
    """
    try:
        # Dump item to pickle
        pickle_file = f"{name}.pickle"
        with open(pickle_file, "wb") as f:
            f.write(pickle.dumps(data))
        return log_artifact(
            project=project_name,
            name=name,
            kind="artifact",
            source=pickle_file,
        )

    except Exception as e:
        msg = f"Some error occurred while logging artifact. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def build_status(
    parsed_execution: dict,
    mapped_outputs: dict | None = None,
) -> dict:
    """
    Collect outputs.

    Parameters
    ----------
    parsed_execution : dict
        Parsed execution dict.
    mapped_outputs : dict
        Mapped outputs.

    Returns
    -------
    dict
        Status dict.
    """
    results = {}
    outputs = {}
    if mapped_outputs is None:
        mapped_outputs = {}

    try:
        for key, _ in mapped_outputs.items():
            if key in parsed_execution:
                if isinstance(parsed_execution[key], (DataitemTable, Artifact)):
                    outputs[key] = parsed_execution[key].key
                else:
                    results[key] = parsed_execution[key]
        return {
            "state": State.COMPLETED.value,
            "outputs": outputs,
            "results": results,
        }
    except Exception as e:
        msg = f"Something got wrong during run status building. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e
