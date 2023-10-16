import pytest


def setup_and_teardown():
    print('\nsetup')
    yield 42
    print('\nteardown')


@pytest.mark.param_scope(setup_and_teardown, None)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_yield(x, param_scope):
    assert param_scope == 42
