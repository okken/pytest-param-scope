import pytest


def foo():
    ...

@pytest.mark.param_scope(foo)
def test_one_params_to_marker():
    """
    This also blows up, with_args required.
    You gotta use `@pytest.mark.param_scope.with_args(foo)`
    """
    ...
