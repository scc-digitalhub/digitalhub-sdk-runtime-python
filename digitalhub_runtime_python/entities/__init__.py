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

function_guardrail_plugin = EntityPlugin(
    builder=FunctionGuardrailBuilder,
    shortcuts=(CrudPlugin(new_function_guardrail),),
)
function_openinference_plugin = EntityPlugin(
    builder=FunctionOpeninferenceBuilder,
    shortcuts=(CrudPlugin(new_function_openinference),),
)
function_python_plugin = EntityPlugin(
    builder=FunctionPythonBuilder,
    shortcuts=(CrudPlugin(new_function_python),),
)

entity_plugins = (
    function_guardrail_plugin,
    function_openinference_plugin,
    function_python_plugin,
    EntityPlugin(builder=TaskGuardrailBuildBuilder),
    EntityPlugin(builder=TaskGuardrailServeBuilder),
    EntityPlugin(builder=TaskOpeninferenceBuildBuilder),
    EntityPlugin(builder=TaskOpeninferenceServeBuilder),
    EntityPlugin(builder=TaskPythonBuildBuilder),
    EntityPlugin(builder=TaskPythonJobBuilder),
    EntityPlugin(builder=TaskPythonServeBuilder),
    EntityPlugin(builder=RunGuardrailRunBuildBuilder),
    EntityPlugin(builder=RunGuardrailRunServeBuilder),
    EntityPlugin(builder=RunOpeninferenceRunBuildBuilder),
    EntityPlugin(builder=RunOpeninferenceRunServeBuilder),
    EntityPlugin(builder=RunPythonRunBuildBuilder),
    EntityPlugin(builder=RunPythonRunJobBuilder),
    EntityPlugin(builder=RunPythonRunServeBuilder),
)
