import pytest


@pytest.fixture(scope='class')
def a_fixture():
    print('\nfixture setup')
    yield 'some data from setup'
    print('\nfixture teardown')


class TestClass():
    @pytest.mark.parametrize('x', ['a', 'b', 'c'])
    def test_param(self, x, a_fixture):
        assert a_fixture == 'some data from setup'