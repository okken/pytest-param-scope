import pytest


def clean_setup():
    print('clean setup')

def error_during_setup():
    print('error during setup')
    a, b = 1, 2
    assert a == b


def clean_teardown():
    print('clean teardown')

def error_during_teardown():
    print('error during teardown')
    a, b = 1, 2
    assert a == b


@pytest.mark.param_scope(error_during_setup, clean_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_error_during_setup(x, param_scope):
    """
    An exception during setup causes an error,
    and teardown is not run
    """
    ...

@pytest.mark.param_scope(clean_setup, error_during_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_error_during_teardown(x):
    """
    An exception during teardown causes an error
    """
    ...


