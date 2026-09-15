# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function.guardrail.builder import FunctionGuardrailBuilder
from digitalhub_runtime_python.entities.function.hydra.builder import FunctionHydraBuilder
from digitalhub_runtime_python.entities.function.openinference.builder import FunctionOpeninferenceBuilder
from digitalhub_runtime_python.entities.function.python.builder import FunctionPythonBuilder
from digitalhub_runtime_python.entities.function.ray.builder import FunctionRayBuilder
from digitalhub_runtime_python.entities.run.guardrail_build.builder import RunGuardrailRunBuildBuilder
from digitalhub_runtime_python.entities.run.guardrail_serve.builder import RunGuardrailRunServeBuilder
from digitalhub_runtime_python.entities.run.hydra_build.builder import RunHydraRunBuildBuilder
from digitalhub_runtime_python.entities.run.hydra_job.builder import RunHydraRunJobBuilder
from digitalhub_runtime_python.entities.run.hydra_subtask.builder import RunHydraRunSubtaskBuilder
from digitalhub_runtime_python.entities.run.openinference_build.builder import RunOpeninferenceRunBuildBuilder
from digitalhub_runtime_python.entities.run.openinference_serve.builder import RunOpeninferenceRunServeBuilder
from digitalhub_runtime_python.entities.run.python_build.builder import RunPythonRunBuildBuilder
from digitalhub_runtime_python.entities.run.python_job.builder import RunPythonRunJobBuilder
from digitalhub_runtime_python.entities.run.python_serve.builder import RunPythonRunServeBuilder
from digitalhub_runtime_python.entities.run.ray_build.builder import RunRayRunBuildBuilder
from digitalhub_runtime_python.entities.run.ray_job.builder import RunRayRunJobBuilder
from digitalhub_runtime_python.entities.task.guardrail_build.builder import TaskGuardrailBuildBuilder
from digitalhub_runtime_python.entities.task.guardrail_serve.builder import TaskGuardrailServeBuilder
from digitalhub_runtime_python.entities.task.hydra_build.builder import TaskHydraBuildBuilder
from digitalhub_runtime_python.entities.task.hydra_job.builder import TaskHydraJobBuilder
from digitalhub_runtime_python.entities.task.hydra_subtask.builder import TaskHydraSubtaskBuilder
from digitalhub_runtime_python.entities.task.openinference_build.builder import TaskOpeninferenceBuildBuilder
from digitalhub_runtime_python.entities.task.openinference_serve.builder import TaskOpeninferenceServeBuilder
from digitalhub_runtime_python.entities.task.python_build.builder import TaskPythonBuildBuilder
from digitalhub_runtime_python.entities.task.python_job.builder import TaskPythonJobBuilder
from digitalhub_runtime_python.entities.task.python_serve.builder import TaskPythonServeBuilder
from digitalhub_runtime_python.entities.task.ray_build.builder import TaskRayBuildBuilder
from digitalhub_runtime_python.entities.task.ray_job.builder import TaskRayJobBuilder

entity_builders = (
    (EntityKinds.FUNCTION_GUARDRAIL.value, FunctionGuardrailBuilder),
    (EntityKinds.FUNCTION_OPENINFERENCE.value, FunctionOpeninferenceBuilder),
    (EntityKinds.FUNCTION_PYTHON.value, FunctionPythonBuilder),
    (EntityKinds.FUNCTION_HYDRA.value, FunctionHydraBuilder),
    (EntityKinds.FUNCTION_RAY.value, FunctionRayBuilder),
    (EntityKinds.RUN_GUARDRAIL_BUILD.value, RunGuardrailRunBuildBuilder),
    (EntityKinds.RUN_GUARDRAIL_SERVE.value, RunGuardrailRunServeBuilder),
    (EntityKinds.RUN_OPENINFERENCE_BUILD.value, RunOpeninferenceRunBuildBuilder),
    (EntityKinds.RUN_OPENINFERENCE_SERVE.value, RunOpeninferenceRunServeBuilder),
    (EntityKinds.RUN_PYTHON_BUILD.value, RunPythonRunBuildBuilder),
    (EntityKinds.RUN_PYTHON_JOB.value, RunPythonRunJobBuilder),
    (EntityKinds.RUN_PYTHON_SERVE.value, RunPythonRunServeBuilder),
    (EntityKinds.RUN_HYDRA_BUILD.value, RunHydraRunBuildBuilder),
    (EntityKinds.RUN_HYDRA_JOB.value, RunHydraRunJobBuilder),
    (EntityKinds.RUN_HYDRA_SUBTASK.value, RunHydraRunSubtaskBuilder),
    (EntityKinds.RUN_RAY_JOB.value, RunRayRunJobBuilder),
    (EntityKinds.RUN_RAY_BUILD.value, RunRayRunBuildBuilder),
    (EntityKinds.TASK_GUARDRAIL_BUILD.value, TaskGuardrailBuildBuilder),
    (EntityKinds.TASK_GUARDRAIL_SERVE.value, TaskGuardrailServeBuilder),
    (EntityKinds.TASK_OPENINFERENCE_BUILD.value, TaskOpeninferenceBuildBuilder),
    (EntityKinds.TASK_OPENINFERENCE_SERVE.value, TaskOpeninferenceServeBuilder),
    (EntityKinds.TASK_PYTHON_BUILD.value, TaskPythonBuildBuilder),
    (EntityKinds.TASK_PYTHON_JOB.value, TaskPythonJobBuilder),
    (EntityKinds.TASK_PYTHON_SERVE.value, TaskPythonServeBuilder),
    (EntityKinds.TASK_HYDRA_BUILD.value, TaskHydraBuildBuilder),
    (EntityKinds.TASK_HYDRA_JOB.value, TaskHydraJobBuilder),
    (EntityKinds.TASK_HYDRA_SUBTASK.value, TaskHydraSubtaskBuilder),
    (EntityKinds.TASK_RAY_BUILD.value, TaskRayBuildBuilder),
    (EntityKinds.TASK_RAY_JOB.value, TaskRayJobBuilder),
)

try:
    from digitalhub_runtime_python.runtimes.builder import (
        RuntimeGuardrailBuilder,
        RuntimeHydraBuilder,
        RuntimeHydraJobBuilder,
        RuntimeHydraSubtaskBuilder,
        RuntimeOpeninferenceBuilder,
        RuntimePythonBuilder,
        RuntimePythonJobBuilder,
        RuntimeRayBuilder,
    )

    runtime_builders = (
        (EntityKinds.FUNCTION_GUARDRAIL.value, RuntimeGuardrailBuilder),
        (EntityKinds.FUNCTION_OPENINFERENCE.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.FUNCTION_PYTHON.value, RuntimePythonBuilder),
        (EntityKinds.FUNCTION_HYDRA.value, RuntimeHydraBuilder),
        (EntityKinds.FUNCTION_RAY.value, RuntimeRayBuilder),
        (EntityKinds.RUN_GUARDRAIL_BUILD.value, RuntimeGuardrailBuilder),
        (EntityKinds.RUN_GUARDRAIL_SERVE.value, RuntimeGuardrailBuilder),
        (EntityKinds.RUN_OPENINFERENCE_BUILD.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.RUN_OPENINFERENCE_SERVE.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.RUN_PYTHON_BUILD.value, RuntimePythonBuilder),
        (EntityKinds.RUN_PYTHON_JOB.value, RuntimePythonJobBuilder),
        (EntityKinds.RUN_PYTHON_SERVE.value, RuntimePythonBuilder),
        (EntityKinds.RUN_HYDRA_BUILD.value, RuntimeHydraBuilder),
        (EntityKinds.RUN_HYDRA_JOB.value, RuntimeHydraJobBuilder),
        (EntityKinds.RUN_HYDRA_SUBTASK.value, RuntimeHydraSubtaskBuilder),
        (EntityKinds.RUN_RAY_BUILD.value, RuntimeRayBuilder),
        (EntityKinds.RUN_RAY_JOB.value, RuntimeRayBuilder),
        (EntityKinds.TASK_GUARDRAIL_BUILD.value, RuntimeGuardrailBuilder),
        (EntityKinds.TASK_GUARDRAIL_SERVE.value, RuntimeGuardrailBuilder),
        (EntityKinds.TASK_OPENINFERENCE_BUILD.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.TASK_OPENINFERENCE_SERVE.value, RuntimeOpeninferenceBuilder),
        (EntityKinds.TASK_PYTHON_BUILD.value, RuntimePythonBuilder),
        (EntityKinds.TASK_PYTHON_JOB.value, RuntimePythonJobBuilder),
        (EntityKinds.TASK_PYTHON_SERVE.value, RuntimePythonBuilder),
        (EntityKinds.TASK_HYDRA_BUILD.value, RuntimeHydraBuilder),
        (EntityKinds.TASK_HYDRA_JOB.value, RuntimeHydraJobBuilder),
        (EntityKinds.TASK_HYDRA_SUBTASK.value, RuntimeHydraSubtaskBuilder),
        (EntityKinds.TASK_RAY_BUILD.value, RuntimeRayBuilder),
        (EntityKinds.TASK_RAY_JOB.value, RuntimeRayBuilder),
    )
except ImportError as e:
    from digitalhub.utils.logger.logger import get_logger

    logger = get_logger(__name__)
    logger.debug(f"Error importing runtime builders: {e}")
    runtime_builders = ()
