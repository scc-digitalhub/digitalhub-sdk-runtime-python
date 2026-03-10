# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function.openinference.entity import FunctionOpeninference
from digitalhub_runtime_python.entities.function.openinference.spec import (
    FunctionSpecOpeninference,
    FunctionValidatorOpeninference,
)
from digitalhub_runtime_python.entities.function.openinference.status import FunctionStatusOpeninference
from digitalhub_runtime_python.entities.function.python.utils import source_check, source_post_check


class FunctionOpeninferenceBuilder(FunctionBuilder, RuntimeEntityBuilderOpeninference):
    """
    FunctionOpeninference builder.
    """

    ENTITY_CLASS = FunctionOpeninference
    ENTITY_SPEC_CLASS = FunctionSpecOpeninference
    ENTITY_SPEC_VALIDATOR = FunctionValidatorOpeninference
    ENTITY_STATUS_CLASS = FunctionStatusOpeninference
    ENTITY_KIND = EntityKinds.FUNCTION_OPENINFERENCE.value

    def build(
        self,
        kind: str,
        project: str,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = False,
        **kwargs,
    ) -> FunctionOpeninference:
        kwargs = source_check(**kwargs)
        obj = super().build(
            kind,
            project,
            name,
            uuid,
            description,
            labels,
            embedded,
            **kwargs,
        )
        return source_post_check(obj)

    def from_dict(self, obj: dict) -> FunctionOpeninference:
        """
        Create a new object from dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        FunctionOpeninference
            Object instance.
        """
        entity = super().from_dict(obj)
        return source_post_check(entity)

    def _parse_dict(self, obj: dict) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        # Look for source in spec
        if spec_dict := obj.get("spec", {}):
            # Check source
            source = spec_dict.get("source", {})
            if source:
                spec_dict["source"] = source_check(source=source)["source"]

        return super()._parse_dict(obj)
