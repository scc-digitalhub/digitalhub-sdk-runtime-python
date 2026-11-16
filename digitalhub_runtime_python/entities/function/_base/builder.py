# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._mixin.source.builder import SourceBuilderMixin
from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilder


class FunctionBaseBuilder(SourceBuilderMixin, FunctionBuilder, RuntimeEntityBuilder):
    """
    Base builder for runtime Python functions.
    """
