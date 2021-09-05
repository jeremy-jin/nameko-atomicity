import eventlet
from eventlet import Event

import pytest
from mock import Mock
from nameko.rpc import rpc
from nameko.testing.services import entrypoint_hook

from nameko_atomicity.rollback_commands import (
    RollbackCommands,
    rollback_once_failed,
)


class TestRollbackCommands:
    @pytest.fixture
    def tracker(self):
        return Mock()

    @pytest.fixture(params=["dependency", "dependency_proxy"])
    def service_class(self, request, tracker):
        class ExampleService:
            name = "exampleservice"

            rollback_commands = RollbackCommands()

            @rollback_once_failed
            @rpc
            def calculate(self, data):
                self.rollback_commands.append(
                    func=self._calculate, args=(data,), kwargs={}
                )
                data["release"].wait()
                raise Exception("Boom!")

            @rollback_once_failed
            @rpc
            def calculate_no_raise(self, data):
                self.rollback_commands.append(
                    func=self._calculate, args=(data,), kwargs={}
                )
                data["release"].wait()

            def _calculate(self, data):
                tracker(data)

        class ExampleServiceUsingProxyDecorator:
            name = "exampleservice"

            rollback_commands = RollbackCommands()

            @rollback_once_failed()
            @rpc
            def calculate(self, data):
                self.rollback_commands.append(
                    func=self._calculate, args=(data,), kwargs={}
                )
                data["release"].wait()
                raise Exception("Boom!")

            @rollback_once_failed()
            @rpc
            def calculate_no_raise(self, data):
                self.rollback_commands.append(
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

    def test_rollback_after_commit_end_to_end(
        self, rabbit_config, container_factory, service_class, tracker
    ):
        release_one, release_two = Event(), Event()

        container = container_factory(service_class, rabbit_config)
        container.start()

        def make_coroutine(release):
            def coroutine():
                with entrypoint_hook(container, "calculate") as calculate:
                    data = {"id": 222, "release": release}
                    calculate(data)

            return coroutine

        def make_coroutine_no_raise(release):
            def coroutine():
                with entrypoint_hook(
                    container, "calculate_no_raise"
                ) as calculate_no_raise:
                    data = {"id": 222, "release": release}
                    calculate_no_raise(data)

            return coroutine

        coroutine_one = make_coroutine(release_one)
        assert 0 == tracker.call_count

        thread_one = eventlet.spawn(coroutine_one)
        eventlet.sleep(0.1)

        release_one.send()
        pytest.raises(Exception, thread_one.wait)
        assert 1 == tracker.call_count

        # no raise
        coroutine_two = make_coroutine_no_raise(release_two)
        assert 1 == tracker.call_count

        thread_two = eventlet.spawn(coroutine_two)
        eventlet.sleep(0.1)

        release_two.send()
        thread_two.wait()
        assert 1 == tracker.call_count
