import sys

import pytest
from digitalhub.plugins import Spec

from digitalhub_runtime_python.entities.function._base.models import PythonSourceCode, PythonVersion
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec
from digitalhub_runtime_python.entities.function.guardrail.models import ProcessingMode
from digitalhub_runtime_python.entities.function.guardrail.spec import FunctionSpecGuardrail
from digitalhub_runtime_python.entities.function.openinference.spec import (
    FunctionSpecOpeninference,
)
from digitalhub_runtime_python.entities.function.python.entity import FunctionPython

CURRENT_PYTHON_VERSION = f"PYTHON{sys.version_info.major}_{sys.version_info.minor}"


def test_function_specs_leave_python_version_unset():
    source = PythonSourceCode(source="source.py", handler="predict")

    assert FunctionBaseSpec(source=source).python_version is None
    assert FunctionSpecGuardrail(source=source, processing_mode=ProcessingMode.PREPROCESSOR).python_version is None
    assert FunctionSpecOpeninference(source=source).python_version is None


def test_function_specs_share_base_spec():
    assert FunctionSpecGuardrail.__bases__[0] is FunctionBaseSpec
    assert FunctionSpecOpeninference.__bases__[0] is FunctionBaseSpec


@pytest.mark.parametrize(
    "spec_class",
    [FunctionBaseSpec, FunctionSpecGuardrail, FunctionSpecOpeninference],
)
def test_function_specs_allow_python_version_to_be_unset(spec_class):
    field = spec_class.model_fields["python_version"]

    assert field.annotation == PythonVersion | None
    assert field.default is None


@pytest.mark.parametrize(
    "spec_class",
    [FunctionBaseSpec, FunctionSpecGuardrail, FunctionSpecOpeninference],
)
def test_function_specs_keep_shared_source_field(spec_class):
    assert spec_class.model_fields["source"].annotation is PythonSourceCode


def test_python_version_validator_returns_value_string():
    spec = FunctionBaseSpec(
        source=PythonSourceCode(source="source.py", handler="predict"),
        python_version=PythonVersion.PYTHON3_11,
    )

    assert isinstance(spec.python_version, str)
    assert spec.python_version == PythonVersion.PYTHON3_11.value


def test_function_base_spec_is_a_pydantic_spec():
    assert issubclass(FunctionBaseSpec, Spec)
    assert "source" in FunctionBaseSpec.model_fields


def test_pre_save_hook_defaults_python_version_to_current():
    function = object.__new__(FunctionPython)
    function.spec = FunctionBaseSpec(
        source=PythonSourceCode(source="source.py", handler="predict"),
        requirements=[],
    )

    function._post_create_hook_before_save()

    assert function.spec.python_version == CURRENT_PYTHON_VERSION


def test_local_execution_rejects_mismatched_python_version_from_spec():
    mismatch = next(version.value for version in PythonVersion if version.value != CURRENT_PYTHON_VERSION)
    function = object.__new__(FunctionPython)
    function.spec = FunctionBaseSpec(
        source=PythonSourceCode(source="source.py", handler="predict"),
        python_version=mismatch,
    )

    with pytest.raises(ValueError, match="Local execution"):
        function.run("run", local_execution=True)
