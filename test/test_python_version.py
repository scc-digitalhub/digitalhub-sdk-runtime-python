import sys

import pytest

from digitalhub_runtime_python.entities.function._base.entity import FunctionBaseFunction
from digitalhub_runtime_python.entities.function._base.models import PythonVersion, SourceValidator
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseValidator
from digitalhub_runtime_python.entities.function.guardrail.spec import FunctionSpecGuardrail, FunctionValidatorGuardrail
from digitalhub_runtime_python.entities.function.openinference.spec import (
    FunctionSpecOpeninference,
    FunctionValidatorOpeninference,
)
from digitalhub_runtime_python.entities.function.python.spec import FunctionSpecPython, FunctionValidatorPython

CURRENT_PYTHON_VERSION = f"PYTHON{sys.version_info.major}_{sys.version_info.minor}"


def test_function_specs_leave_python_version_unset():
    assert FunctionSpecPython().python_version is None
    assert FunctionSpecGuardrail().python_version is None
    assert FunctionSpecOpeninference().python_version is None


def test_function_specs_share_base_spec():
    base_spec = FunctionSpecPython.__bases__[0]

    assert base_spec.__name__ == "FunctionBaseSpec"
    assert FunctionSpecGuardrail.__bases__[0] is base_spec
    assert FunctionSpecOpeninference.__bases__[0] is base_spec


@pytest.mark.parametrize(
    "validator",
    [FunctionValidatorPython, FunctionValidatorGuardrail, FunctionValidatorOpeninference],
)
def test_function_validators_allow_python_version_to_be_unset(validator):
    field = validator.model_fields["python_version"]

    assert field.annotation == PythonVersion | None
    assert field.default is None


@pytest.mark.parametrize(
    "validator",
    [FunctionValidatorPython, FunctionValidatorGuardrail, FunctionValidatorOpeninference],
)
def test_function_validators_keep_shared_source_field(validator):
    assert validator.model_fields["source"].annotation is SourceValidator


def test_python_version_validator_returns_value_string():
    validator = FunctionValidatorPython.model_validate(
        {"source": {}, "python_version": PythonVersion.PYTHON3_11},
    )

    assert isinstance(validator.python_version, str)
    assert validator.python_version == PythonVersion.PYTHON3_11.value


def test_function_validators_share_base_validator():
    assert issubclass(FunctionValidatorPython, FunctionBaseValidator)
    assert issubclass(FunctionValidatorGuardrail, FunctionBaseValidator)
    assert issubclass(FunctionValidatorOpeninference, FunctionBaseValidator)


def test_pre_save_hook_defaults_python_version_to_current():
    function = object.__new__(FunctionBaseFunction)
    function.spec = FunctionSpecPython(requirements=[])

    function._post_create_hook_before_save()

    assert function.spec.python_version == CURRENT_PYTHON_VERSION


def test_local_execution_rejects_mismatched_python_version_from_spec():
    mismatch = next(version.value for version in PythonVersion if version.value != CURRENT_PYTHON_VERSION)
    function = object.__new__(FunctionBaseFunction)
    function.spec = FunctionSpecPython(python_version=mismatch)

    with pytest.raises(ValueError, match="Local execution"):
        function.run("run", local_execution=True)
