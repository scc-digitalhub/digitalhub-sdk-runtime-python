# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import BuildSpecMixin, ServeSpecMixin, TaskSpecFunction
from pydantic import Field


class TaskSpecBuild(TaskSpecFunction, BuildSpecMixin):
    """Shared build-task specification."""


class TaskSpecServe(TaskSpecFunction, ServeSpecMixin):
    """Shared serve-task specification."""

    replicas: int | None = Field(default=None, ge=1)
