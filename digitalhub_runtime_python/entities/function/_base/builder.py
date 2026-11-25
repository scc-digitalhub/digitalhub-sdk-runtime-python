# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import FunctionBuilder, SourceBuilderMixin

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilder


class FunctionBaseBuilder(SourceBuilderMixin, FunctionBuilder, RuntimeEntityBuilder):
    """
    Base builder for runtime Python functions.
    """
