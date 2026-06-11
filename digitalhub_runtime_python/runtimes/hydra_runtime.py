import sys
from typing import Callable

from digitalhub_runtime_python.runtimes.runtime import RuntimePython, RuntimePythonJob

from digitalhub_runtime_python.utils.configuration import (
    DEFAULT_PY_FILE, _get_function_path, _import_function_from_path, has_git_scheme, has_remote_scheme, has_s3_scheme, 
    _clone_git_source, _download_remote_source, _download_s3_source
)

from digitalhub.utils.generic_utils import (
    decode_base64_string
)


class RuntimeHydra(RuntimePython):
    """
    Runtime Hydra class.
    """

class RuntimeHydraJob(RuntimePythonJob):
    """
    Runtime Hydra Job class.
    """

    def _configure_execution(self, spec: dict) -> tuple[Callable, bool]:
        args = ["main", "-m", "hydra/launcher=dh"]

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


        fnc, _ = super()._configure_execution(spec)
        # treat as not wrapped, as the wrapping is done by hydra.main and we do not need to pass the extra attributes
        return fnc, False

    def _compose_args(self, func, spec, project):
        # we call without any parameters
        args = {"cfg_passthrough": None}
        return args 


class RuntimeHydraSubtask(RuntimePythonJob):
    """
    Runtime Hydra Subtask class.
    """
    def _configure_execution(self, spec: dict) -> tuple[Callable, bool]:
        source_spec = spec.get("source", {})
        base64 = source_spec.get("base64")
        path = self.runtime_dir

        # no source re-creation, assume already exists in runtime dir
        if base64 is not None:
            path = path / DEFAULT_PY_FILE

        function_path, function_name = _get_function_path(path, source_spec["handler"])
        fnc = _import_function_from_path(function_path, function_name)
        # treat as not wrapped, as the wrapping is done by hydra.main and we do not need to pass the extra attributes
        return fnc, False

    def _compose_args(self, func, spec, project):
        # expect to be wrapped with hydra.main, 'cfg' is in the parameters, and Omecaconf is present
        import OmegaConf
        args = super()._compose_args(func, spec, project)
        args["cfg_passthrough"] = OmegaConf.to_container(spec.get("parameters", {}).get("cfg", {}))
        return args 
    