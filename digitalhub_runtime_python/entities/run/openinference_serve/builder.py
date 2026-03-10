# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.openinference_serve.entity import RunOpeninferenceRunServe
from digitalhub_runtime_python.entities.run.openinference_serve.spec import (
    RunSpecOpeninferenceRunServe,
    RunValidatorOpeninferenceRunServe,
)
from digitalhub_runtime_python.entities.run.openinference_serve.status import RunStatusOpeninferenceRunServe


class RunOpeninferenceRunServeBuilder(RunBuilder, RuntimeEntityBuilderOpeninference):
    """
    RunOpeninferenceRunServeBuilder runner.
    """

    ENTITY_CLASS = RunOpeninferenceRunServe
    ENTITY_SPEC_CLASS = RunSpecOpeninferenceRunServe
    ENTITY_SPEC_VALIDATOR = RunValidatorOpeninferenceRunServe
    ENTITY_STATUS_CLASS = RunStatusOpeninferenceRunServe
    ENTITY_KIND = EntityKinds.RUN_OPENINFERENCE_SERVE.value
