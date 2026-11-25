from types import SimpleNamespace
from unittest.mock import Mock

from digitalhub.context.context import Context
from digitalhub.plugins import Relationship, State

import digitalhub_runtime_python.utils.outputs as outputs_module


def test_build_new_status_includes_context_registered_entities(monkeypatch) -> None:
    project = SimpleNamespace(
        name="project",
        _client=Mock(),
        spec=SimpleNamespace(config={}, source="."),
    )
    context = Context(project)
    context.set_run(SimpleNamespace(key="run-key", id="run-id"))
    entity = SimpleNamespace(name="artifact", key="artifact-key", add_relationship=Mock())
    context.register_entity(entity)
    get_context = Mock(return_value=context)
    monkeypatch.setattr(outputs_module, "get_context", get_context)

    status = outputs_module.build_new_status("project", {"result": 42})

    assert status == {
        "state": State.COMPLETED.value,
        "outputs": {"artifact": "artifact-key"},
        "results": {"result": 42},
    }
    entity.add_relationship.assert_called_once_with(Relationship.PRODUCEDBY.value, "run-key:run-id")
    get_context.assert_called_once_with("project")
