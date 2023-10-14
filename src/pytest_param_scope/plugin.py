import pytest

def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'param_scope(setup, teardown): setup and teardown for parametrized tests')

__parametrized_test = None
__teardown_func = None
__ready_for_teardown = False
__setup_value = None
__exception = None

@pytest.fixture(scope="function")
def param_scope(request):
    global __parametrized_test
    global __teardown_func
    global __ready_for_teardown
    global __setup_value
    global __exception

    # for "test_foo[1]", we just want "test_foo"
    test_name = request.node.name.split("[")[0]

    if __parametrized_test is None:
        # this is the first time, so go ahead and call setup,
        # and save the teardown for later
        setup_func = None
        teardown_func = None

        m = request.node.get_closest_marker("param_scope")
        if m:
            setup_func = m.args[0]
            teardown_func = m.args[1]

        __parametrized_test = test_name

        if setup_func:
            try:
                __setup_value = setup_func()
            except Exception as e:
                __exception = e
                raise e
        else:
            __setup_value = None

        __teardown_func = teardown_func
        __ready_for_teardown = False
        __exception = None
    else:
        if __parametrized_test == test_name:
            if __exception:
                # there was an exception in setup
                # so we need to Error
                raise __exception

    yield __setup_value

    if __ready_for_teardown:
        teardown_func = __teardown_func

        # clean up globals
        __parametrized_test = None
        __teardown_func = None
        __ready_for_teardown = False
        __setup_value = None

        # call teardown
        if teardown_func:
            teardown_func()


def pytest_runtest_teardown(item, nextitem):
    global __ready_for_teardown
    if __parametrized_test:
        if nextitem:
            next_name = nextitem.name.split("[")[0]
        else:
            next_name = None

        if __parametrized_test != next_name:
            __ready_for_teardown = True


def pytest_itemcollected(item):
    m = item.get_closest_marker("param_scope")
    if m and ('param_scope' not in item.fixturenames):
        item.fixturenames.append('param_scope')

