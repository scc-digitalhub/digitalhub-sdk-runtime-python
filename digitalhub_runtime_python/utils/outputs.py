# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pickle
import typing
from dataclasses import dataclass
from typing import Any

from digitalhub import (
    log_croissant,
    log_generic_artifact,
    log_generic_dataitem,
    log_generic_model,
    log_mlflow,
    log_sklearn,
    log_table,
)
from digitalhub.context.api import get_context
from digitalhub.entities._commons.enums import EntityKinds, Relationship, State
from digitalhub.entities.artifact._base.entity import Artifact
from digitalhub.entities.artifact.crud import log_artifact
from digitalhub.entities.dataitem._base.entity import Dataitem
from digitalhub.entities.dataitem.crud import log_dataitem
from digitalhub.entities.model._base.entity import Model
from digitalhub.stores.readers.data.api import get_supported_dataframes
from digitalhub.utils.exceptions import EntityNotExistsError
from digitalhub.utils.logger.logger import get_logger

if typing.TYPE_CHECKING:
    from digitalhub.entities.dataitem.table.entity import DataitemTable

logger = get_logger(__file__)


mapped_logger = {
    EntityKinds.DATAITEM_DATAITEM.value: log_generic_dataitem,
    EntityKinds.DATAITEM_TABLE.value: log_table,
    EntityKinds.DATAITEM_CROISSANT.value: log_croissant,
    EntityKinds.MODEL_MLFLOW.value: log_mlflow,
    EntityKinds.MODEL_SKLEARN.value: log_sklearn,
    EntityKinds.MODEL_MODEL.value: log_generic_model,
    EntityKinds.ARTIFACT_ARTIFACT.value: log_generic_artifact,
}


@dataclass
class OutputStruct:
    """
    OutputStruct is a class that represents the output of a function.
    """

    name: str | None
    kind: str | None
    kwargs: dict | None = None
    log: bool = False


def _build_default_output_names(outputs_len: int, results_len: int) -> list[str]:
    return [f"output_{idx}" for idx in range(outputs_len, results_len)]


def _parse_UDF_outputs(outputs: list[str] | list[dict[str, Any]], results_len: int) -> list[OutputStruct]:
    """
    Parse UDF outputs.

    Parameters
    ----------
    outputs : list[str] | list[dict[str, str]]
        List of named outputs to collect.
    results_len : int
        Number of results produced by the function.

    Returns
    -------
    list[OutputStruct]
        List of OutputStruct objects.
    """
    normalized_outputs = list(outputs[:results_len])

    if len(normalized_outputs) != results_len:
        # Set default names for outputs if the number of outputs is different from the number of results.
        # If the number of outputs is less than the number of results, the missing outputs will be named as output_{idx}.
        # If the number of outputs is greater than the number of results, the extra outputs will be ignored.
        logger.warning(
            f"Number of outputs ({len(outputs)}) is different from number of results ({results_len}). "
            f"Default names will be used for outputs.",
        )
        normalized_outputs.extend(_build_default_output_names(len(normalized_outputs), results_len))

    parsed_outputs = []
    for idx, item in enumerate(normalized_outputs):
        if isinstance(item, str):
            parsed_outputs.append(OutputStruct(name=item, kind=None))
            continue

        if not isinstance(item, dict):
            raise ValueError(f"Invalid output format: {item}")

        name = item.get("name") or f"output_{idx}"
        kind = item.get("kind")
        if kind is None:
            raise ValueError(f"Missing kind for logged output: {name}")

        if kind not in mapped_logger:
            raise ValueError(f"Unsupported output kind: {kind}")

        kwargs = dict(item.get("spec_kwargs") or {})
        parsed_outputs.append(OutputStruct(name=name, kind=kind, kwargs=kwargs, log=True))
    return parsed_outputs


def _log_mapped_output(project_name: str, item: Any, output: OutputStruct) -> None:
    logger.info(f"Logging output {output.name}.")
    spec_kwargs = dict(output.kwargs or {})
    spec_kwargs["source"] = item
    mapped_logger[output.kind](project_name, output.name, **spec_kwargs)


def _save_existing_object(obj: Dataitem | Artifact | Model, run_key: str) -> Dataitem | Artifact | Model:
    dest = run_key + ":" + run_key.split("/")[-1]
    obj.add_relationship(relation=Relationship.PRODUCEDBY.value, dest=dest)

    try:
        obj.save(update=True)
    except EntityNotExistsError:
        obj.save()

    return obj


def _materialize_output(name: str, item: Any, project_name: str, run_key: str) -> Any:
    if isinstance(item, (str, int, float, bool, bytes)):
        return item

    if isinstance(item, (Dataitem, Artifact, Model)):
        return _save_existing_object(item, run_key)

    for df_class in get_supported_dataframes():
        if isinstance(item, df_class):
            return _log_dataitem(name, project_name, item)

    return _log_artifact(name, project_name, item)


def collect_outputs(
    results: Any,
    outputs: list[str] | list[dict[str, Any]],
    project_name: str,
    run_key: str,
) -> dict:
    """
    Collect outputs. Use the produced results directly.

    Parameters
    ----------
    results : Any
        Function outputs.
    outputs : list[OutputStruct]
        List of named outputs to collect.
    project_name : str
        Project name.
    run_key : str
        Run key.

    Returns
    -------
    dict
        Function outputs.
    """
    objects = {}
    results = listify_results(results)

    parsed_outputs = _parse_UDF_outputs(outputs, len(results))

    for idx, item in enumerate(results):
        output = parsed_outputs[idx]

        if output.log:
            _log_mapped_output(project_name, item, output)
            continue

        objects[output.name] = _materialize_output(output.name, item, project_name, run_key)

    return objects


def parse_outputs(results: list, project_name: str, run_key: str) -> dict:
    """
    Parse outputs.

    Parameters
    ----------
    results : list
        Function outputs list.
    project_name : str
        Project name.
    run_key : str
        Run key.

    Returns
    -------
    dict
        Function outputs.
    """
    out_list = [f"output_{idx}" for idx in range(len(listify_results(results)))]
    return collect_outputs(results, out_list, project_name, run_key)


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
        Data.

    Returns
    -------
    str
        Dataitem key.
    """
    try:
        return log_dataitem(
            project=project_name,
            name=name,
            kind=EntityKinds.DATAITEM_TABLE.value,
            data=data,
        )
    except Exception as e:
        msg = f"Some error occurred while logging dataitem. Exception: {e.__class__}. Error: {e.args}"
        logger.exception(msg)
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
            kind=EntityKinds.ARTIFACT_ARTIFACT.value,
            source=pickle_file,
        )

    except Exception as e:
        msg = f"Some error occurred while logging artifact. Exception: {e.__class__}. Error: {e.args}"
        logger.exception(msg)
        raise RuntimeError(msg)


def build_new_status(
    project_name: str,
    parsed_execution: dict,
) -> dict:
    """
    Build run status after execution.

    Parameters
    ----------
    project_name : str
        Project name.
    parsed_execution : dict
        Parsed execution dict.

    Returns
    -------
    dict
        Status dict.
    """
    results = {}
    outputs = {**get_context(project_name).logged}
    try:
        for key, value in parsed_execution.items():
            if isinstance(value, (Dataitem, Artifact, Model)):
                outputs[key] = value.key
            else:
                results[key] = value

        return {
            "state": State.COMPLETED.value,
            "outputs": outputs,
            "results": results,
        }
    except Exception as e:
        msg = f"Something got wrong during run status building. Exception: {e.__class__}. Error: {e.args}"
        logger.exception(msg)
        raise RuntimeError(msg) from e
