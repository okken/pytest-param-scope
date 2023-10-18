from __future__ import annotations
import types
from typing import Generator
import pytest
from dataclasses import dataclass
from typing import Callable, Any


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'param_scope(setup, teardown): setup and teardown for parametrized tests')


@dataclass
class ParamScopeData():
    test_name: str | None = None
    teardown_func: Callable | None = None
    teardown_gen: Generator[Any, None, None] | None = None
    ready_for_teardown: bool = False
    setup_value: Any = None
    exception: Exception | None = None


# current test run
__data = ParamScopeData()


@pytest.fixture(scope="function")
def param_scope(request):
    global __data

    setup_func = None

    # for "test_foo[1]", we just want "test_foo"
    test_name = request.node.name.split("[")[0]

    if __data.test_name is None:
        # this is the first time, so go ahead and call setup,
        # and save the teardown for later
        __data.test_name = test_name

        m = request.node.get_closest_marker("param_scope")
        if m:
            if len(m.args) >= 1:
                setup_func = m.args[0]
            if len(m.args) >= 2:
                __data.teardown_func = m.args[1]

        if setup_func:
            try:
                # setup could be a func, or could be a generator
                setup_value = setup_func()
                if isinstance(setup_value, types.GeneratorType):
                    # if generator, call next() once for setup section
                    new_value = next(setup_value)
                    __data.setup_value = new_value
                    # and save it for teardown
                    __data.teardown_gen = setup_value
                else:
                    # otherwise, just save the value
                    __data.setup_value = setup_value
            except Exception as e:
                __data.exception = e
                raise e
    else:
        if __data.test_name == test_name:
            if __data.exception:
                # there was an exception in setup
                # so we need to Error
                raise  __data.exception

    yield __data.setup_value

    if __data.ready_for_teardown:
        teardown_gen = __data.teardown_gen
        teardown_func = __data.teardown_func

        __data = ParamScopeData()  # reset for next one

        if teardown_gen:
            try:
                next(teardown_gen)
            except StopIteration:
                pass # this is expected


        # should we disallow both a teardown from gen and a teardown?
        # for now, I'll allow it, as it's a bit messy to disallow it
        if teardown_func:
            teardown_func()


def pytest_runtest_teardown(item, nextitem):
    # if next is a new name, it's time for teardown
    if nextitem:
        next_name = nextitem.name.split("[")[0]
    else:
        next_name = None

    if __data.test_name != next_name:
            __data.ready_for_teardown = True


def pytest_itemcollected(item):
    m = item.get_closest_marker("param_scope")
    if m and ('param_scope' not in item.fixturenames):
        item.fixturenames.append('param_scope')

