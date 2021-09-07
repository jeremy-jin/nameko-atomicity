import eventlet
from eventlet import Event

import pytest
from mock import Mock
from nameko.rpc import rpc
from nameko.testing.services import entrypoint_hook

from nameko_atomicity.dispatch_commands import (
    DispatchCommands,
    dispatch_after_commit,
)


class TestDispatchCommands:
    @pytest.fixture
    def tracker(self):
        return Mock()

    @pytest.fixture(params=["dependency", "dependency_proxy"])
    def service_class(self, request, tracker):
        class ExampleService:
            name = "exampleservice"

            dispatch_commands = DispatchCommands()

            @dispatch_after_commit
            @rpc
            def calculate(self, data):
                self.dispatch_commands.append(
                    func=self._calculate, args=(data,), kwargs={}
                )
                data["release"].wait()

            def _calculate(self, data):
                tracker(data)

        class ExampleServiceUsingProxyDecorator:
            name = "exampleservice"

            dispatch_commands = DispatchCommands()

            @dispatch_after_commit()
            @rpc
            def calculate(self, data):
                self.dispatch_commands.append(
                    func=self._calculate, args=(data,), kwargs={}
                )
                data["release"].wait()

            def _calculate(self, data):
                tracker(data)

        services = {
            "dependency": ExampleService,
            "dependency_proxy": ExampleServiceUsingProxyDecorator,
        }

        return services[request.param]

    def test_dispatch_after_commit_end_to_end(
        self, rabbit_config, container_factory, service_class, tracker
    ):
        release_one = Event()

        container = container_factory(service_class, rabbit_config)
        container.start()

        def make_coroutine(release):
            def coroutine():
                with entrypoint_hook(container, "calculate") as calculate:
                    data = {"id": 222, "release": release}
                    calculate(data)

            return coroutine

        coroutine_one = make_coroutine(release_one)
        assert 0 == tracker.call_count

        thread_one = eventlet.spawn(coroutine_one)
        eventlet.sleep(0.1)

        release_one.send()
        thread_one.wait()
        assert 1 == tracker.call_count
