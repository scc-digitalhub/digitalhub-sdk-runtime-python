# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class EntityKinds(Enum):
    """
    Entity kinds.
    """

    FUNCTION_PYTHON = "python"
    TASK_PYTHON_BUILD = "python+build"
    TASK_PYTHON_JOB = "python+job"
    TASK_PYTHON_SERVE = "python+serve"
    RUN_PYTHON_BUILD = "python+build:run"
    RUN_PYTHON_JOB = "python+job:run"
    RUN_PYTHON_SERVE = "python+serve:run"

    FUNCTION_OPENINFERENCE = "openinference"
    TASK_OPENINFERENCE_BUILD = "openinference+build"
    TASK_OPENINFERENCE_SERVE = "openinference+serve"
    RUN_OPENINFERENCE_BUILD = "openinference+build:run"
    RUN_OPENINFERENCE_SERVE = "openinference+serve:run"

    FUNCTION_GUARDRAIL = "guardrail"
    TASK_GUARDRAIL_BUILD = "guardrail+build"
    TASK_GUARDRAIL_SERVE = "guardrail+serve"
    RUN_GUARDRAIL_BUILD = "guardrail+build:run"
    RUN_GUARDRAIL_SERVE = "guardrail+serve:run"


class Actions(Enum):
    """
    Task actions.
    """

    BUILD = "build"
    JOB = "job"
    SERVE = "serve"
