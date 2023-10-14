import pytest

def param_setup():
    print('\nparam setup')
    return 'some data from setup'

def param_teardown():
    print('\nparam teardown')


@pytest.mark.param_scope(param_setup, param_teardown)
def test_foo():
   ...

def test_just_to_make_param_scope_work():
   ...

