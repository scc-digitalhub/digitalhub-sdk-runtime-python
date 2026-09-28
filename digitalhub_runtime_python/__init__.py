# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_python.entities import entity_plugins
from digitalhub_runtime_python.entities._commons.enums import EntityKinds

entity_builders = tuple((plugin.kind, plugin.builder) for plugin in entity_plugins)

try:
    from digitalhub_runtime_python.runtimes.builder import (
        RuntimeGuardrailBuilder,
        RuntimeOpeninferenceBuilder,
        RuntimePythonBuilder,
        RuntimePythonJobBuilder,
    )

    runtime_builders = (
        (EntityKinds.FUNCTION_GUARDRAIL.value, RuntimeGuardrailBuilder),
        (EntityKinds.FUNCTION_OPENINFERENCE.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.FUNCTION_PYTHON.value, RuntimePythonBuilder),
        (EntityKinds.RUN_GUARDRAIL_BUILD.value, RuntimeGuardrailBuilder),
        (EntityKinds.RUN_GUARDRAIL_SERVE.value, RuntimeGuardrailBuilder),
        (EntityKinds.RUN_OPENINFERENCE_BUILD.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.RUN_OPENINFERENCE_SERVE.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.RUN_PYTHON_BUILD.value, RuntimePythonBuilder),
        (EntityKinds.RUN_PYTHON_JOB.value, RuntimePythonJobBuilder),
        (EntityKinds.RUN_PYTHON_SERVE.value, RuntimePythonBuilder),
        (EntityKinds.TASK_GUARDRAIL_BUILD.value, RuntimeGuardrailBuilder),
        (EntityKinds.TASK_GUARDRAIL_SERVE.value, RuntimeGuardrailBuilder),
        (EntityKinds.TASK_OPENINFERENCE_BUILD.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.TASK_OPENINFERENCE_SERVE.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.TASK_PYTHON_BUILD.value, RuntimePythonBuilder),
        (EntityKinds.TASK_PYTHON_JOB.value, RuntimePythonJobBuilder),
        (EntityKinds.TASK_PYTHON_SERVE.value, RuntimePythonBuilder),
    )
except ImportError as e:
    from digitalhub.utils.logger.logger import get_logger

    logger = get_logger(__name__)
    logger.debug(f"Error importing runtime builders: {e}")
    runtime_builders = tuple()
