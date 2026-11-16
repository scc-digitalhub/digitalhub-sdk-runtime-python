import pytest
from digitalhub.entities._constructors.spec import build_spec
from pydantic import ValidationError

from digitalhub_runtime_python.entities.function._base import utils as function_utils
from digitalhub_runtime_python.entities.function._base.models import SourceValidator
from digitalhub_runtime_python.entities.function.guardrail.models import ProcessingMode
from digitalhub_runtime_python.entities.function.guardrail.spec import FunctionSpecGuardrail
from digitalhub_runtime_python.entities.function.openinference.models import TensorValidator
from digitalhub_runtime_python.entities.function.openinference.spec import FunctionSpecOpeninference
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
            source=SourceValidator(),
            unknown_parameter=True,
        )


def test_function_specs_validate_action_fields_and_roundtrip():
    with pytest.raises(ValidationError):
        FunctionSpecGuardrail(source=SourceValidator())

    guardrail = FunctionSpecGuardrail(
        source=SourceValidator(),
        processing_mode=ProcessingMode.PREPROCESSOR,
    )
    openinference = FunctionSpecOpeninference(
        source={"handler": "predict"},
        inputs=[{"name": "features"}],
    )
    restored = FunctionSpecOpeninference.from_dict(openinference.to_dict())

    assert guardrail.processing_mode == ProcessingMode.PREPROCESSOR.value
    assert isinstance(openinference.inputs[0], TensorValidator)
    assert openinference.outputs == []
    assert restored.source.handler == "predict"
    assert restored.inputs[0].name == "features"


def test_source_export_restores_base64_when_export_raises(monkeypatch, tmp_path):
    source = SourceValidator(source="source.py", base64="c2NyaXB0")
    monkeypatch.setattr(function_utils, "has_local_scheme", lambda _: True)
    monkeypatch.setattr(function_utils, "write_text", lambda *args: None)

    with pytest.raises(RuntimeError, match="export failed"), function_utils.export_local_source(source, tmp_path):
        assert source.base64 is None
        raise RuntimeError("export failed")

    assert source.base64 == "c2NyaXB0"


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

    with pytest.raises(TypeError, match="instructions"):
        build_spec(RunSpecPythonRunBuild, task="task", instructions=["apt-get update"])

    with pytest.raises(TypeError, match="service_type"):
        build_spec(RunSpecPythonRunServe, task="task", service_type="NodePort")

    with pytest.raises(TypeError, match="replicas"):
        build_spec(RunSpecGuardrailRunServe, task="task", replicas=2)

    with pytest.raises(TypeError, match="instructions"):
        build_spec(RunSpecOpeninferenceRunBuild, task="task", instructions=["apt-get update"])


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
