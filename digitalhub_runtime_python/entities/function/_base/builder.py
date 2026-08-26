# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub_runtime_python.entities._commons.utils import source_check, source_post_check


class FunctionBaseBuilder(FunctionBuilder, RuntimeEntityBuilder):
    """
    Base builder for runtime Python functions.
    """

    def _prepare_kwargs(self, kwargs: dict) -> dict:
        return source_check(**kwargs)

    def _prepare_source(self, source: dict) -> dict:
        return source_check(source=source)["source"]

    def build(self, *args, **kwargs):
        kwargs = self._prepare_kwargs(kwargs)
        return source_post_check(super().build(*args, **kwargs))

    def from_dict(self, obj: dict):
        return source_post_check(super().from_dict(obj))

    def _parse_dict(self, obj: dict) -> dict:
        if spec_dict := obj.get("spec", {}):
            # Check source
            source = spec_dict.get("source", {})
            if source:
                spec_dict["source"] = self._prepare_source(source)

        return super()._parse_dict(obj)
