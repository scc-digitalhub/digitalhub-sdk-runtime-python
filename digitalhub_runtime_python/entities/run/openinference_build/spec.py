# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecOpeninferenceRunBuild(RunSpec):
    """RunSpecOpeninferenceRunBuild specifications."""

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
        model_name: str | None = None,
        inputs: list | None = None,
        outputs: list | None = None,
        instructions: dict | None = None,
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
        self.model_name = model_name
        self.inputs = inputs
        self.outputs = outputs
        self.instructions = instructions
        self.init_parameters = init_parameters


class RunValidatorOpeninferenceRunBuild(RunValidator):
    """RunValidatorOpeninferenceRunBuild validator."""

    # Function parameters
    source: dict | None = None
    image: str | None = None
    base_image: str | None = None
    python_version: str | None = None
    requirements: list | None = None
    model_name: str | None = None
    inputs: list | None = None
    outputs: list | None = None

    # Task parameters
    instructions: dict | None = None

    # Run parameters
    init_parameters: dict | None = None
    """Initialization parameters"""
