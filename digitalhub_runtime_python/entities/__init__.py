# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from digitalhub.plugins import (
    Action,
    BuilderDef,
    CrudPlugin,
    ExecFamily,
    FunctionBuilder,
    RunBuilder,
    SourceBuilderMixin,
    Status,
    TaskBuilder,
    TaskSpecFunction,
)

from digitalhub_runtime_python.entities._commons.enums import Actions, EntityKinds
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec
from digitalhub_runtime_python.entities.function.guardrail.crud import new_function_guardrail
from digitalhub_runtime_python.entities.function.guardrail.entity import FunctionGuardrail
from digitalhub_runtime_python.entities.function.guardrail.spec import FunctionSpecGuardrail
from digitalhub_runtime_python.entities.function.openinference.crud import new_function_openinference
from digitalhub_runtime_python.entities.function.openinference.entity import FunctionOpeninference
from digitalhub_runtime_python.entities.function.openinference.spec import FunctionSpecOpeninference
from digitalhub_runtime_python.entities.function.python.crud import new_function_python
from digitalhub_runtime_python.entities.function.python.entity import FunctionPython
from digitalhub_runtime_python.entities.run._base.status import RunStatusBaseRun
from digitalhub_runtime_python.entities.run.guardrail_build.entity import RunGuardrailRunBuild
from digitalhub_runtime_python.entities.run.guardrail_build.spec import RunSpecGuardrailRunBuild
from digitalhub_runtime_python.entities.run.guardrail_serve.entity import RunGuardrailRunServe
from digitalhub_runtime_python.entities.run.guardrail_serve.spec import RunSpecGuardrailRunServe
from digitalhub_runtime_python.entities.run.openinference_build.entity import RunOpeninferenceRunBuild
from digitalhub_runtime_python.entities.run.openinference_build.spec import RunSpecOpeninferenceRunBuild
from digitalhub_runtime_python.entities.run.openinference_serve.entity import RunOpeninferenceRunServe
from digitalhub_runtime_python.entities.run.openinference_serve.spec import RunSpecOpeninferenceRunServe
from digitalhub_runtime_python.entities.run.python_build.entity import RunPythonRunBuild
from digitalhub_runtime_python.entities.run.python_build.spec import RunSpecPythonRunBuild
from digitalhub_runtime_python.entities.run.python_job.entity import RunPythonRunJob
from digitalhub_runtime_python.entities.run.python_job.spec import RunSpecPythonRunJob
from digitalhub_runtime_python.entities.run.python_serve.entity import RunPythonRunServe
from digitalhub_runtime_python.entities.run.python_serve.spec import RunSpecPythonRunServe
from digitalhub_runtime_python.entities.task._base.spec import TaskSpecBuild, TaskSpecServe
from digitalhub_runtime_python.entities.task.guardrail_build.entity import TaskGuardrailBuild
from digitalhub_runtime_python.entities.task.guardrail_serve.entity import TaskGuardrailServe
from digitalhub_runtime_python.entities.task.openinference_build.entity import TaskOpeninferenceBuild
from digitalhub_runtime_python.entities.task.openinference_serve.entity import TaskOpeninferenceServe
from digitalhub_runtime_python.entities.task.python_build.entity import TaskPythonBuild
from digitalhub_runtime_python.entities.task.python_job.entity import TaskPythonJob
from digitalhub_runtime_python.entities.task.python_serve.entity import TaskPythonServe

# Imported on first use: the entities register even when the runtime cannot be
# imported, and the import error is reported when a run executes locally.
RUNTIME_GUARDRAIL_BUILDER = "digitalhub_runtime_python.runtimes.builder:RuntimeGuardrailBuilder"
RUNTIME_OPENINFERENCE_BUILDER = "digitalhub_runtime_python.runtimes.builder:RuntimeOpeninferenceBuilder"
RUNTIME_PYTHON_BUILDER = "digitalhub_runtime_python.runtimes.builder:RuntimePythonBuilder"
RUNTIME_PYTHON_JOB_BUILDER = "digitalhub_runtime_python.runtimes.builder:RuntimePythonJobBuilder"

guardrail = ExecFamily(
    executable=BuilderDef(
        EntityKinds.FUNCTION_GUARDRAIL,
        FunctionGuardrail,
        FunctionSpecGuardrail,
        Status,
        base=FunctionBuilder,
        mixins=(SourceBuilderMixin,),
        shortcuts=(CrudPlugin(new_function_guardrail),),
    ),
    actions={
        Actions.BUILD: Action(
            task=BuilderDef(
                EntityKinds.TASK_GUARDRAIL_BUILD, TaskGuardrailBuild, TaskSpecBuild, Status, base=TaskBuilder
            ),
            run=BuilderDef(
                EntityKinds.RUN_GUARDRAIL_BUILD,
                RunGuardrailRunBuild,
                RunSpecGuardrailRunBuild,
                RunStatusBaseRun,
                base=RunBuilder,
            ),
        ),
        Actions.SERVE: Action(
            task=BuilderDef(
                EntityKinds.TASK_GUARDRAIL_SERVE, TaskGuardrailServe, TaskSpecServe, Status, base=TaskBuilder
            ),
            run=BuilderDef(
                EntityKinds.RUN_GUARDRAIL_SERVE,
                RunGuardrailRunServe,
                RunSpecGuardrailRunServe,
                RunStatusBaseRun,
                base=RunBuilder,
            ),
        ),
    },
    runtime_builder=RUNTIME_GUARDRAIL_BUILDER,
)

openinference = ExecFamily(
    executable=BuilderDef(
        EntityKinds.FUNCTION_OPENINFERENCE,
        FunctionOpeninference,
        FunctionSpecOpeninference,
        Status,
        base=FunctionBuilder,
        mixins=(SourceBuilderMixin,),
        shortcuts=(CrudPlugin(new_function_openinference),),
    ),
    actions={
        Actions.BUILD: Action(
            task=BuilderDef(
                EntityKinds.TASK_OPENINFERENCE_BUILD, TaskOpeninferenceBuild, TaskSpecBuild, Status, base=TaskBuilder
            ),
            run=BuilderDef(
                EntityKinds.RUN_OPENINFERENCE_BUILD,
                RunOpeninferenceRunBuild,
                RunSpecOpeninferenceRunBuild,
                RunStatusBaseRun,
                base=RunBuilder,
            ),
        ),
        Actions.SERVE: Action(
            task=BuilderDef(
                EntityKinds.TASK_OPENINFERENCE_SERVE, TaskOpeninferenceServe, TaskSpecServe, Status, base=TaskBuilder
            ),
            run=BuilderDef(
                EntityKinds.RUN_OPENINFERENCE_SERVE,
                RunOpeninferenceRunServe,
                RunSpecOpeninferenceRunServe,
                RunStatusBaseRun,
                base=RunBuilder,
            ),
        ),
    },
    runtime_builder=RUNTIME_OPENINFERENCE_BUILDER,
)

python = ExecFamily(
    executable=BuilderDef(
        EntityKinds.FUNCTION_PYTHON,
        FunctionPython,
        FunctionBaseSpec,
        Status,
        base=FunctionBuilder,
        mixins=(SourceBuilderMixin,),
        shortcuts=(CrudPlugin(new_function_python),),
    ),
    actions={
        Actions.JOB: Action(
            task=BuilderDef(EntityKinds.TASK_PYTHON_JOB, TaskPythonJob, TaskSpecFunction, Status, base=TaskBuilder),
            run=BuilderDef(
                EntityKinds.RUN_PYTHON_JOB, RunPythonRunJob, RunSpecPythonRunJob, RunStatusBaseRun, base=RunBuilder
            ),
            runtime_builder=RUNTIME_PYTHON_JOB_BUILDER,
        ),
        Actions.BUILD: Action(
            task=BuilderDef(EntityKinds.TASK_PYTHON_BUILD, TaskPythonBuild, TaskSpecBuild, Status, base=TaskBuilder),
            run=BuilderDef(
                EntityKinds.RUN_PYTHON_BUILD,
                RunPythonRunBuild,
                RunSpecPythonRunBuild,
                RunStatusBaseRun,
                base=RunBuilder,
            ),
        ),
        Actions.SERVE: Action(
            task=BuilderDef(EntityKinds.TASK_PYTHON_SERVE, TaskPythonServe, TaskSpecServe, Status, base=TaskBuilder),
            run=BuilderDef(
                EntityKinds.RUN_PYTHON_SERVE,
                RunPythonRunServe,
                RunSpecPythonRunServe,
                RunStatusBaseRun,
                base=RunBuilder,
            ),
        ),
    },
    runtime_builder=RUNTIME_PYTHON_BUILDER,
)

entity_plugins = (
    *guardrail.plugins(),
    *openinference.plugins(),
    *python.plugins(),
)
