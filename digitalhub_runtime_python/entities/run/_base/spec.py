# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecPythonRun(RunSpec):
    """RunSpecPythonRun specifications."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
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
        service_type: str | None = None,
        service_name: str | None = None,
        replicas: int | None = None,
        instructions: dict | None = None,
        inputs: dict | None = None,
        parameters: dict | None = None,
        init_parameters: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            local_execution,
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
        self.service_type = service_type
        self.service_name = service_name
        self.replicas = replicas
        self.instructions = instructions
        self.inputs = inputs
        self.parameters = parameters
        self.init_parameters = init_parameters


class RunValidatorPythonRun(RunValidator):
    """RunValidatorPythonRun validator."""

    # Function parameters
    source: dict | None = None
    image: str | None = None
    base_image: str | None = None
    python_version: str | None = None
    requirements: list | None = None

    # Task serve
    service_type: str | None = None
    service_name: str | None = None
    replicas: int | None = None

    # Task build
    instructions: list[str] | None = None

    # Run parameters
    inputs: dict | None = None
    """Run inputs."""

    parameters: dict | None = None
    """Run parameters."""

    init_parameters: dict | None = None
    """Init function parameters."""
