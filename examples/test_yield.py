import pytest


def setup_and_teardown():
    print('\nsetup')
    yield 42
    print('\nteardown')


@pytest.mark.param_scope(setup_and_teardown, None)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_yield(x, param_scope):
    assert param_scope == 42



def separate_teardown():
    print('separate teardown')


@pytest.mark.param_scope(setup_and_teardown, separate_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_two_teardowns(x, param_scope):
    """
    For now, we'll allow this odd use model.
    Weird, but really, why not?
    """
    assert param_scope == 42


@pytest.mark.param_scope.with_args(setup_and_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_just_one_func(x, param_scope):
    """
    It's not pretty, but if you want to just pass in one,
    you gotta use "with_args".
    See "Passing a callable to custom markers" in pytest docs
    - https://docs.pytest.org/en/stable/example/markers.html#passing-a-callable-to-custom-markers
    """
    assert param_scope == 42


@pytest.mark.param_scope
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_no_param_scope_args(x):
    """
    No point in this, but it doesn't blow up
    """
    ...
