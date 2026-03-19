# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function.guardrail.builder import FunctionGuardrailBuilder
from digitalhub_runtime_python.entities.function.openinference.builder import FunctionOpeninferenceBuilder
from digitalhub_runtime_python.entities.function.python.builder import FunctionPythonBuilder
from digitalhub_runtime_python.entities.run.guardrail_build.builder import RunGuardrailRunBuildBuilder
from digitalhub_runtime_python.entities.run.guardrail_serve.builder import RunGuardrailRunServeBuilder
from digitalhub_runtime_python.entities.run.openinference_build.builder import RunOpeninferenceRunBuildBuilder
from digitalhub_runtime_python.entities.run.openinference_serve.builder import RunOpeninferenceRunServeBuilder
from digitalhub_runtime_python.entities.run.python_build.builder import RunPythonRunBuildBuilder
from digitalhub_runtime_python.entities.run.python_job.builder import RunPythonRunJobBuilder
from digitalhub_runtime_python.entities.run.python_serve.builder import RunPythonRunServeBuilder
from digitalhub_runtime_python.entities.task.guardrail_build.builder import TaskGuardrailBuildBuilder
from digitalhub_runtime_python.entities.task.guardrail_serve.builder import TaskGuardrailServeBuilder
from digitalhub_runtime_python.entities.task.openinference_build.builder import TaskOpeninferenceBuildBuilder
from digitalhub_runtime_python.entities.task.openinference_serve.builder import TaskOpeninferenceServeBuilder
from digitalhub_runtime_python.entities.task.python_build.builder import TaskPythonBuildBuilder
from digitalhub_runtime_python.entities.task.python_job.builder import TaskPythonJobBuilder
from digitalhub_runtime_python.entities.task.python_serve.builder import TaskPythonServeBuilder
from digitalhub_runtime_python.utils.utils import handler, parse_requirements

entity_builders = (
    (EntityKinds.FUNCTION_GUARDRAIL.value, FunctionGuardrailBuilder),
    (EntityKinds.FUNCTION_OPENINFERENCE.value, FunctionOpeninferenceBuilder),
    (EntityKinds.FUNCTION_PYTHON.value, FunctionPythonBuilder),
    (EntityKinds.RUN_GUARDRAIL_BUILD.value, RunGuardrailRunBuildBuilder),
    (EntityKinds.RUN_GUARDRAIL_SERVE.value, RunGuardrailRunServeBuilder),
    (EntityKinds.RUN_OPENINFERENCE_BUILD.value, RunOpeninferenceRunBuildBuilder),
    (EntityKinds.RUN_OPENINFERENCE_SERVE.value, RunOpeninferenceRunServeBuilder),
    (EntityKinds.RUN_PYTHON_BUILD.value, RunPythonRunBuildBuilder),
    (EntityKinds.RUN_PYTHON_JOB.value, RunPythonRunJobBuilder),
    (EntityKinds.RUN_PYTHON_SERVE.value, RunPythonRunServeBuilder),
    (EntityKinds.TASK_GUARDRAIL_BUILD.value, TaskGuardrailBuildBuilder),
    (EntityKinds.TASK_GUARDRAIL_SERVE.value, TaskGuardrailServeBuilder),
    (EntityKinds.TASK_OPENINFERENCE_BUILD.value, TaskOpeninferenceBuildBuilder),
    (EntityKinds.TASK_OPENINFERENCE_SERVE.value, TaskOpeninferenceServeBuilder),
    (EntityKinds.TASK_PYTHON_BUILD.value, TaskPythonBuildBuilder),
    (EntityKinds.TASK_PYTHON_JOB.value, TaskPythonJobBuilder),
    (EntityKinds.TASK_PYTHON_SERVE.value, TaskPythonServeBuilder),
)

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
