# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecGuardrailRunBuild(RunSpec):
    """RunSpecGuardrailRunBuild specifications."""

    def __init__(
        self,
        task: str,
        function: str | None = None,
        workflow: str | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        python_version: str | None = None,
        requirements: list | None = None,
        processing_mode: str | None = None,
        instructions: list | None = None,
        init_parameters: dict | None = None,
        **kwargs,
    ):
        super().__init__(
            task,
            function,
            workflow,
            volumes,
            resources,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.source = source
        self.image = image
        self.base_image = base_image
        self.python_version = python_version
        self.requirements = requirements
        self.instructions = instructions
        self.processing_mode = processing_mode
        self.init_parameters = init_parameters


class RunValidatorGuardrailRunBuild(RunValidator):
    """RunValidatorGuardrailRunBuild validator."""

    # Function parameters
    source: dict | None = None
    image: str | None = None
    base_image: str | None = None
    python_version: str | None = None
    requirements: list | None = None
    processing_mode: str | None = None

    # Task parameters
    instructions: list | None = None

    # Run parameters
    init_parameters: dict | None = None
    """Init parameters."""
