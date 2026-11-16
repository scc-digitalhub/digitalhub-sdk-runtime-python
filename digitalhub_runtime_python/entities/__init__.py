# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.factory.plugins import CrudPlugin, EntityPlugin

from digitalhub_runtime_python.entities.function.guardrail.builder import FunctionGuardrailBuilder
from digitalhub_runtime_python.entities.function.guardrail.crud import new_function_guardrail
from digitalhub_runtime_python.entities.function.openinference.builder import FunctionOpeninferenceBuilder
from digitalhub_runtime_python.entities.function.openinference.crud import new_function_openinference
from digitalhub_runtime_python.entities.function.python.builder import FunctionPythonBuilder
from digitalhub_runtime_python.entities.function.python.crud import new_function_python
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

try:
    from digitalhub_runtime_python.runtimes.builder import (
        RuntimeGuardrailBuilder,
        RuntimeOpeninferenceBuilder,
        RuntimePythonBuilder,
        RuntimePythonJobBuilder,
    )
except ImportError as e:
    from digitalhub.utils.logger.logger import get_logger

    get_logger(__name__).debug(f"Error importing runtime builders: {e}")
    RuntimeGuardrailBuilder = None
    RuntimeOpeninferenceBuilder = None
    RuntimePythonBuilder = None
    RuntimePythonJobBuilder = None

function_guardrail_plugin = EntityPlugin(
    builder=FunctionGuardrailBuilder,
    shortcuts=(CrudPlugin(new_function_guardrail),),
    runtime_builder=RuntimeGuardrailBuilder,
)
function_openinference_plugin = EntityPlugin(
    builder=FunctionOpeninferenceBuilder,
    shortcuts=(CrudPlugin(new_function_openinference),),
    runtime_builder=RuntimeOpeninferenceBuilder,
)
function_python_plugin = EntityPlugin(
    builder=FunctionPythonBuilder,
    shortcuts=(CrudPlugin(new_function_python),),
    runtime_builder=RuntimePythonBuilder,
)

entity_plugins = (
    function_guardrail_plugin,
    function_openinference_plugin,
    function_python_plugin,
    EntityPlugin(builder=TaskGuardrailBuildBuilder, runtime_builder=RuntimeGuardrailBuilder),
    EntityPlugin(builder=TaskGuardrailServeBuilder, runtime_builder=RuntimeGuardrailBuilder),
    EntityPlugin(builder=TaskOpeninferenceBuildBuilder, runtime_builder=RuntimeOpeninferenceBuilder),
    EntityPlugin(builder=TaskOpeninferenceServeBuilder, runtime_builder=RuntimeOpeninferenceBuilder),
    EntityPlugin(builder=TaskPythonBuildBuilder, runtime_builder=RuntimePythonBuilder),
    EntityPlugin(builder=TaskPythonJobBuilder, runtime_builder=RuntimePythonJobBuilder),
    EntityPlugin(builder=TaskPythonServeBuilder, runtime_builder=RuntimePythonBuilder),
    EntityPlugin(builder=RunGuardrailRunBuildBuilder, runtime_builder=RuntimeGuardrailBuilder),
    EntityPlugin(builder=RunGuardrailRunServeBuilder, runtime_builder=RuntimeGuardrailBuilder),
    EntityPlugin(builder=RunOpeninferenceRunBuildBuilder, runtime_builder=RuntimeOpeninferenceBuilder),
    EntityPlugin(builder=RunOpeninferenceRunServeBuilder, runtime_builder=RuntimeOpeninferenceBuilder),
    EntityPlugin(builder=RunPythonRunBuildBuilder, runtime_builder=RuntimePythonBuilder),
    EntityPlugin(builder=RunPythonRunJobBuilder, runtime_builder=RuntimePythonJobBuilder),
    EntityPlugin(builder=RunPythonRunServeBuilder, runtime_builder=RuntimePythonBuilder),
)
