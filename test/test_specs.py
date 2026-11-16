from types import SimpleNamespace
from unittest.mock import Mock

import digitalhub.entities._mixin.source.entity as source_entity_module
import pytest
from digitalhub.entities._constructors.spec import build_spec
from digitalhub.entities.function._base.entity import Function
from pydantic import ValidationError

import digitalhub_runtime_python.entities.function._base.entity as function_entity_module
from digitalhub_runtime_python.entities.function._base.entity import FunctionBaseFunction
from digitalhub_runtime_python.entities.function._base.models import SourceValidator
from digitalhub_runtime_python.entities.function.guardrail.models import ProcessingMode
from digitalhub_runtime_python.entities.function.guardrail.spec import FunctionSpecGuardrail
from digitalhub_runtime_python.entities.function.openinference.models import TensorValidator
from digitalhub_runtime_python.entities.function.openinference.spec import FunctionSpecOpeninference
from digitalhub_runtime_python.entities.function.python.builder import FunctionPythonBuilder
from digitalhub_runtime_python.entities.function.python.spec import FunctionSpecPython
from digitalhub_runtime_python.entities.run.guardrail_serve.spec import RunSpecGuardrailRunServe
from digitalhub_runtime_python.entities.run.openinference_build.spec import RunSpecOpeninferenceRunBuild
from digitalhub_runtime_python.entities.run.python_build.spec import RunSpecPythonRunBuild
from digitalhub_runtime_python.entities.run.python_job.spec import RunSpecPythonRunJob
from digitalhub_runtime_python.entities.run.python_serve.spec import RunSpecPythonRunServe
from digitalhub_runtime_python.entities.task.python_build.spec import TaskSpecPythonBuild
from digitalhub_runtime_python.entities.task.python_serve.spec import TaskSpecPythonServe


def test_function_spec_rejects_unknown_build_parameters():
    with pytest.raises(TypeError, match="unknown_parameter"):
        build_spec(
            FunctionSpecPython,
            source=SourceValidator(source="source.py", handler="predict"),
            unknown_parameter=True,
        )

def test_function_specs_validate_action_fields_and_roundtrip():
    with pytest.raises(ValidationError):
        FunctionSpecGuardrail(source=SourceValidator(source="source.py", handler="predict"))

    guardrail = FunctionSpecGuardrail(
        source=SourceValidator(source="source.py", handler="predict"),
        processing_mode=ProcessingMode.PREPROCESSOR,
    )
    openinference = FunctionSpecOpeninference(
        source={"source": "source.py", "handler": "predict"},
        inputs=[{"name": "features"}],
    )
    restored = FunctionSpecOpeninference.from_dict(openinference.to_dict())

    assert guardrail.processing_mode == ProcessingMode.PREPROCESSOR.value
    assert isinstance(openinference.inputs[0], TensorValidator)
    assert openinference.outputs == []
    assert restored.source.handler == "predict"
    assert restored.inputs[0].name == "features"


def test_source_export_restores_base64_when_export_raises(monkeypatch, tmp_path):
    source = SourceValidator(source="source.py", handler="predict", base64="c2NyaXB0")
    function = object.__new__(FunctionBaseFunction)
    function.spec = SimpleNamespace(source=source)
    function._context = Mock(return_value=SimpleNamespace(root=tmp_path))
    monkeypatch.setattr(source_entity_module, "has_local_scheme", lambda _: True)
    monkeypatch.setattr(source_entity_module, "write_text", lambda *args: None)
    monkeypatch.setattr(Function, "export", Mock(side_effect=RuntimeError("export failed")))

    with pytest.raises(RuntimeError, match="export failed"):
        function.export()
    assert source.base64 == "c2NyaXB0"


def test_python_builder_routes_top_level_source_arguments():
    builder = FunctionPythonBuilder()

    function = builder.build(
        kind=builder.ENTITY_KIND,
        project="project",
        name="function",
        code="print('hello')",
        handler="main",
        init_function="initialize",
    )

    assert function.spec.source.base64 == "cHJpbnQoJ2hlbGxvJyk="
    assert function.spec.source.handler == "main"
    assert function.spec.source.init_function == "initialize"


def test_function_export_omits_config_base64_without_mutating_original(monkeypatch, tmp_path):
    original_config = {"base64": "c2VjcmV0", "path": "config.yaml"}
    function = object.__new__(FunctionBaseFunction)
    function.spec = SimpleNamespace(
        config=original_config,
        source=SourceValidator(source="remote-source", handler="predict"),
    )
    function._context = Mock(return_value=SimpleNamespace(root=tmp_path))
    monkeypatch.setattr(function_entity_module, "write_text", Mock())

    def export(self):
        assert self.spec.config == {"path": "config.yaml"}
        return "exported"

    monkeypatch.setattr(Function, "export", export)

    assert function.export() == "exported"
    assert function.spec.config is original_config
    assert original_config == {"base64": "c2VjcmV0", "path": "config.yaml"}


def test_function_export_restores_original_config_when_write_fails(monkeypatch, tmp_path):
    original_config = {"base64": "c2VjcmV0", "path": "config.yaml"}
    function = object.__new__(FunctionBaseFunction)
    function.spec = SimpleNamespace(
        config=original_config,
        source=SourceValidator(source="remote-source", handler="predict"),
    )
    function._context = Mock(return_value=SimpleNamespace(root=tmp_path))
    monkeypatch.setattr(function_entity_module, "write_text", Mock(side_effect=OSError("write failed")))

    with pytest.raises(OSError, match="write failed"):
        function.export()

    assert function.spec.config is original_config
    assert original_config == {"base64": "c2VjcmV0", "path": "config.yaml"}


def test_task_specs_validate_action_fields():
    build = build_spec(TaskSpecPythonBuild, function="function", instructions=["apt-get update"])
    serve = build_spec(
        TaskSpecPythonServe,
        function="function",
        replicas=2,
        service_type="NodePort",
    )

    assert build.instructions == ["apt-get update"]
    assert serve.replicas == 2
    assert serve.service_type == "NodePort"

    with pytest.raises(ValidationError):
        build_spec(TaskSpecPythonServe, function="function", replicas=0)


def test_task_and_run_parameters_are_not_interchangeable():
    with pytest.raises(TypeError, match="service_type"):
        build_spec(TaskSpecPythonBuild, function="function", service_type="NodePort")

    build = build_spec(RunSpecPythonRunBuild, task="task", instructions=["apt-get update"])
    serve = build_spec(
        RunSpecPythonRunServe,
        task="task",
        replicas=2,
        service_type="NodePort",
    )
    guardrail_serve = build_spec(RunSpecGuardrailRunServe, task="task", replicas=2)
    openinference_build = build_spec(
        RunSpecOpeninferenceRunBuild,
        task="task",
        instructions=["apt-get update"],
    )

    assert build.instructions == ["apt-get update"]
    assert serve.replicas == 2
    assert serve.service_type == "NodePort"
    assert guardrail_serve.replicas == 2
    assert openinference_build.instructions == ["apt-get update"]

    with pytest.raises(TypeError, match="instructions"):
        build_spec(RunSpecPythonRunJob, task="task", instructions=["apt-get update"])

    with pytest.raises(TypeError, match="replicas"):
        build_spec(RunSpecPythonRunJob, task="task", replicas=2)


def test_python_run_specs_keep_run_parameters():
    build = build_spec(
        RunSpecPythonRunBuild,
        task="task",
        inputs={"input": "value"},
        parameters={"parameter": "value"},
    )
    job = build_spec(
        RunSpecPythonRunJob,
        task="task",
        local_execution=True,
    )

    assert build.inputs == {"input": "value"}
    assert build.parameters == {"parameter": "value"}
    assert job.local_execution is True


def test_run_spec_reads_legacy_task_fields():
    spec = RunSpecPythonRunBuild.from_dict(
        {
            "task": "task",
            "instructions": ["legacy build instruction"],
            "service_type": "NodePort",
        }
    )

    assert spec.to_dict()["instructions"] == ["legacy build instruction"]
    assert spec.to_dict()["service_type"] == "NodePort"
