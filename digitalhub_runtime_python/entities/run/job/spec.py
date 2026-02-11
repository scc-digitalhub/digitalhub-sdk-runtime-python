# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities.run._base.spec import RunSpecPythonRun, RunValidatorPythonRun


class RunSpecPythonRunJob(RunSpecPythonRun):
    """RunSpecPythonRunJob specifications."""

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
        service_type: str | None = None,
        service_name: str | None = None,
        replicas: int | None = None,
        instructions: dict | None = None,
        inputs: dict | None = None,
        parameters: dict | None = None,
        init_parameters: dict | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            function,
            workflow,
            volumes,
            resources,
            envs,
            secrets,
            profile,
            source,
            image,
            base_image,
            python_version,
            requirements,
            service_type,
            service_name,
            replicas,
            instructions,
            inputs,
            parameters,
            init_parameters,
            **kwargs,
        )
        self.local_execution = local_execution


class RunValidatorPythonRunJob(RunValidatorPythonRun):
    """RunValidatorPythonRunJob validator."""

    local_execution: bool = False
    """Whether to execute the run locally instead of in the cluster."""
