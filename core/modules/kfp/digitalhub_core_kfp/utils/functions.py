from __future__ import annotations

import os
import time
import tempfile
from typing import Callable
import yaml

import kfp
from kfp.compiler import compiler

from digitalhub_core_kfp.dsl import set_current_project, unset_current_project
from digitalhub_core_kfp.utils.outputs import build_status

from digitalhub_core.utils.io_utils import read_yaml, write_yaml
from digitalhub_core.entities.runs.entity import Run

import digitalhub as dhcore

def build_kfp_pipeline(run: dict, pipeline: Callable) -> any:
    """
    Build KFP pipeline.

    Parameters
    ----------
    run: dict
        Run definition.
    pipeline : Callable
        KFP pipeline function.

    """
    pipeline_spec = None
    with tempfile.TemporaryDirectory() as tmpdir:
        pipeline_package_path = os.path.join(tmpdir, 'pipeline.yaml')
        # workaround to pass the project implicitly
        set_current_project(run.get("project"))
        compiler.Compiler(kfp.dsl.PipelineExecutionMode.V1_LEGACY).compile(
            pipeline_func=pipeline,
            package_path=pipeline_package_path
        )
        unset_current_project()
        pipeline_spec = read_yaml(pipeline_package_path)
    return pipeline_spec

def run_kfp_pipeline(run: dict) -> any:
    """
    Run KFP pipeline.

    Parameters
    ----------
    pipeline : BaseRuntime
        KFP pipeline function.
    pipeline_args : dict
        Pipeline arguments.

    Returns
    -------
    dict
        Execution results.
    """

    def _kfp_execution(pipeline: Callable, function_args) -> dict:
        client = kfp.Client(host=os.environ.get("KFP_ENDPOINT"))
        # workaround to pass the project implicitly
        workflow = run.get("spec", {}).get("pipeline_spec", {}).get("workflow", None)
        # workflow was not built locally, need to replicate the build
        if workflow is None:
            dhcore_run = dhcore.get_run(run.get("project"), run.get("id"))
            workflow = build_kfp_pipeline(run, pipeline)
            run_dict = dhcore_run.to_dict()
            run_dict["spec"]["pipeline_spec"]["workflow"] = workflow
            dhcore_run.spec = Run.from_dict(run_dict, validate=False).spec
            # update spec
            dhcore_run.save(update=True)


        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline_package_path = os.path.join(tmpdir, 'pipeline.yaml')
            write_yaml(pipeline_package_path, workflow)
            result = client.create_run_from_pipeline_package(pipeline_package_path, arguments=function_args)

        status = None
        response = None
        run_status = None
        while status is None or status.lower() not in ["succeeded", "failed", "skipped", "error"]:
            time.sleep(5)
            try:
                response = client.get_run(run_id=result.run_id)
                status = response.run.status
                run_status = build_status(response, client)
                # update status
                dhcore_run = dhcore.get_run(run.get("project"), run.get("id"))
                dhcore_run._set_status(run_status)
                dhcore_run.save(update=True)
            except Exception:
                pass
        return run_status

    return _kfp_execution
