# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.runtimes.builder import RuntimeBuilder

from digitalhub_runtime_python.runtimes.runtime import (
    RuntimeGuardrail,
    RuntimeOpeninference,
    RuntimePython,
    RuntimePythonJob,
)

from digitalhub_runtime_python.runtimes.hydra_runtime import (
    RuntimeHydra,
    RuntimeHydraJob,
    RuntimeHydraSubtask,
)

class RuntimePythonBuilder(RuntimeBuilder):
    """RuntimePythonBuilder class."""

    RUNTIME_CLASS = RuntimePython


class RuntimePythonJobBuilder(RuntimeBuilder):
    """RuntimePythonJobBuilder class."""

    RUNTIME_CLASS = RuntimePythonJob


class RuntimeOpeninferenceBuilder(RuntimeBuilder):
    """RuntimeOpeninferenceBuilder class."""

    RUNTIME_CLASS = RuntimeOpeninference


class RuntimeGuardrailBuilder(RuntimeBuilder):
    """RuntimeGuardrailBuilder class."""

    RUNTIME_CLASS = RuntimeGuardrail

class RuntimeHydraBuilder(RuntimeBuilder):
    """RuntimeHydraBuilder class."""

    RUNTIME_CLASS = RuntimeHydra

class RuntimeHydraJobBuilder(RuntimeBuilder):
    """RuntimeHydraJobBuilder class."""

    RUNTIME_CLASS = RuntimeHydraJob

class RuntimeHydraSubtaskBuilder(RuntimeBuilder):
    """RuntimeHydraSubtaskBuilder class."""

    RUNTIME_CLASS = RuntimeHydraSubtask
    