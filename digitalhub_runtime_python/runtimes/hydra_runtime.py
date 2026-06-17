import sys
from typing import Callable
import yaml

from digitalhub_runtime_python.runtimes.runtime import RuntimePython, RuntimePythonJob

from digitalhub_runtime_python.utils.configuration import (
    DEFAULT_PY_FILE, _get_function_path, _import_function_from_path, has_git_scheme, has_remote_scheme, has_s3_scheme, 
    _clone_git_source, _download_remote_source, _download_s3_source
)

from digitalhub.utils.generic_utils import (
    decode_base64_string
)
from digitalhub.utils.logger.logger import get_logger

from digitalhub_runtime_python.utils.outputs import build_new_status, collect_outputs


logger = get_logger(__file__)

class RuntimeHydra(RuntimePython):
    """
    Runtime Hydra class.
    """

class RuntimeHydraJob(RuntimePythonJob):
    """
    Runtime Hydra Job class.
    """

    def run(self, run: dict) -> dict:
        """
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        logger.info("Validating task.")
        self._validate_task(run)

        logger.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")
        run_key = run.get("key")

        logger.info("Configuring execution.")
        fnc, fnc_args = self._configure_execution(spec, run)

        logger.info("Executing run.")
        exec_result = self._execute(fnc, **fnc_args)
        logger.info("Collecting outputs.")
        named_outputs = self._get_named_outputs(exec_result)
        results = collect_outputs(exec_result, named_outputs, project, run_key)
        status = build_new_status(project, results)

        # Return run status
        logger.info("Task completed, returning run status.")
        return status

    def _configure_execution(self, spec: dict, run: dict) -> tuple[Callable, bool]:
        args = ["main", "-m"]

        # write runtime config for dh launcher
        dh_launcher_config = {
            "defaults": ["dh"],
            "n_jobs": spec.get("workers", 1),
            "function": spec.get("function", "hydra"),
            "project_name": self.project,
            "local_execution": True,
        }
        extra_conf_dir = self.runtime_dir / "dh_extra_conf" / "hydra" / "launcher"
        extra_conf_dir.mkdir(parents=True, exist_ok=True)
        with open(extra_conf_dir / "dh_launcher.yaml", "w") as outfile:
            yaml.dump(dh_launcher_config, outfile, default_flow_style=False)

        if "config" in spec:
            config = spec["config"]
            # Here we handle a specific situation: main and config are provided and loaded to the runtime_dir
            # In this case we need anticipate the command line arguments overwriting the config path and config name
            if "base64" in config:
                base64_content = config["base64"]
                path = self.runtime_dir
                file_path = path / "config.yaml"
                file_path.write_text(decode_base64_string(base64_content))
                # Call overwriting the launcher and other overwrites
                # but with dh launcher, multirun, run execution attributes, and custom overwrites
                sys.argv = args + [f"--config-path={path.absolute()}", f"--config-name=config"]
            
            # download config to runtime dir
            elif "source" in config:
                path = self.runtime_dir / "config"
                source = config["source"]
                if has_git_scheme(source):
                    _clone_git_source(path, source)
                # Remote HTTP(S) source
                elif has_remote_scheme(source):
                    _download_remote_source(path, source)
                # S3 source
                elif has_s3_scheme(source):
                    _download_s3_source(path, source)
                # Unsupported scheme
                else:
                    raise RuntimeError(f"Unable to collect source from: {source}")
                sys.argv = args + [f"--config-path={path.absolute()}"]
            elif "path" in config:
                path = self.runtime_dir / config["path"]
                sys.argv = args + [f"--config-path={path.absolute()}"]

        sys.argv += [f"--config-dir={(self.runtime_dir / "dh_extra_conf" ).absolute()}", "hydra/launcher=dh_launcher", f"hydra.launcher.job_ref={run['id']}"]

        fnc, _ = super()._configure_execution(spec)
        # treat as not wrapped, as the wrapping is done by hydra.main and we do not need to pass the extra attributes
        return fnc, {"cfg_passthrough": None}

class RuntimeHydraSubtask(RuntimePythonJob):
    """
    Runtime Hydra Subtask class.
    """
    def _configure_execution(self, spec: dict) -> tuple[Callable, bool]:
        source_spec = spec.get("source", {})
        path = self.runtime_dir

        function_path, function_name = _get_function_path(path, source_spec["handler"])
        fnc = _import_function_from_path(function_path, function_name)
        # treat as not wrapped, as the wrapping is done by hydra.main and we do not need to pass the extra attributes
        return fnc, False

    def _compose_args(self, func, spec, project):
        # expect to be wrapped with hydra.main, 'cfg' is in the parameters, and Omecaconf is present
        from omegaconf import OmegaConf
        args = super()._compose_args(func, spec, project)
        try:
            import omegaconf
            args["cfg_passthrough"] = OmegaConf.create(spec.get("parameters", {}).get("cfg_passthrough", {}))
        except Exception as e:
            print(f"Failed to convert cfg to container. Exception: {e.__class__}. Error: {e.args}")
            args["cfg_passthrough"] = {}
        return args 
    