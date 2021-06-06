import pytest
from mock import Mock
from nameko.containers import ServiceContainer

from nameko_atomicity import DispatchCommands, RollbackCommands


@pytest.fixture
def config():
    return {}


@pytest.fixture
def container(config):
    return Mock(spec=ServiceContainer, config=config, service_name="exampleservice")


@pytest.fixture
def worker_ctx(container):
    worker_ctx = Mock()
    worker_ctx.container = container
    return worker_ctx


@pytest.fixture
def dispatch_commands(container):
    dependency = DispatchCommands().bind(container, "dispatch_commands")
    setattr(container, "dispatch_commands", dependency)
    return dependency


@pytest.fixture
def rollback_commands(container):
    dependency = RollbackCommands().bind(container, "rollback_commands")
    setattr(container, "rollback_commands", dependency)
    return dependency


@pytest.fixture
def func():
    return Mock()
