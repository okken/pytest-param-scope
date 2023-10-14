import pytest


def param_setup():
    print('\nparam setup')
    return 'some data from setup'

def param_teardown():
    print('\nparam teardown')



@pytest.mark.param_scope(param_setup, param_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_param(x, param_scope):
    """
    mark.param_scope is used to pass
    setup and teardown functions to fixture

    param_scope fixture is necessary if you
    want to use the value from setup
    """
    assert param_scope == 'some data from setup'



@pytest.mark.param_scope(param_setup, param_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
class TestClass():
    """also works with classes"""

    def test_method_1(self, x):
        ...

    def test_method_2(self, x):
        ...


@pytest.mark.param_scope(param_setup, param_teardown)
def test_no_param(param_scope):
    """
    marking a test without parametrization
    acts just like a function scope fixture
    """
    assert param_scope == 'some data from setup'


@pytest.mark.param_scope(None, param_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_no_setup(x):
    """
    It's ok for setup to be None
    """
    ...


@pytest.mark.param_scope(param_setup, None)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_no_teardown(x):
    """
    It's ok for teardown to be None
    """
    ...


@pytest.mark.param_scope(None, None)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_no_setup_nor_teardown(x):
    """
    Both setup and teardown can be None
    But really, what's the point?
    """
    ...


def test_no_param_no_mark():
    """
    Just a normal test
    """
    ...


def test_fixture_but_no_mark(param_scope):
    """
    fixture should be a no-op
    """
    ...


