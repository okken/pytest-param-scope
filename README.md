# pytest-param-scope

The pytest parametrize scope fixture workaround.

----

`pytest-param-scope` provides a `param_scope` marker to pass setup and teardown functions to a parametrized function.

There's also a `param_scope` fixture to allow the return value of the setup function to be passed to the test.

## Installation

From PyPI:

```
$ pip install pytest-param-scope
```

## Example


```python
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
```

**Let's see it run:**

```shell
(venv) $ pytest -s -v test_param_scope.py::test_param
================== test session starts ===================
collected 3 items                                        

test_param_scope.py::test_param[a] 
param setup
PASSED
test_param_scope.py::test_param[b] PASSED
test_param_scope.py::test_param[c] PASSED
param teardown

=================== 3 passed in 0.01s ====================

```

**What are we seeing?**

1. Setup is run before the first parameter in a set.
2. Teardown is run after the last parameter.
3. The `param_scope` fixture holds the return value of the setup function.


## Similarities to Fixtures

* Teardown is not run if the setup fails.
* Setup is run once, even though the value can be retrieved by all parametrized test cases.
* If an exception occurs in setup, the test will report Error and not run. The teardown will also not run.
* If an exception occurs in teardown, the LAST parametrized test case to run results in BOTH PASS and Error. This is weird, but consistent with pytest fixtures.


## You can combine setup and teardown in one function

You can provide a function separated by a `yield` to put both setup and teardown in one function.

However, there's a trick to doing this:

* Either, pass `None` as the teardown.
* Or use `with_args`, as in `@pytest.mark.param_scope.with_args(my_func)`

Here's a combo setup/teardown function:

```python
def setup_and_teardown():
    print('\nsetup')
    yield 42
    print('\nteardown')

```

Calling it with `None` for teardown:

```python
import pytest

@pytest.mark.param_scope(setup_and_teardown, None)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_yield(x, param_scope):
    assert param_scope == 42

```

Or using `with_args`:

```python
@pytest.mark.param_scope.with_args(setup_and_teardown)
@pytest.mark.parametrize('x', ['a', 'b', 'c'])
def test_just_one_func(x, param_scope):
    assert param_scope == 42

```

Both of these examples are in `examples/test_yield.py`.



## More examples

Please see `examples` directory in the repo.


## Limitations

The implementation is a total hack and relies on global variables and looking up the next test to see when to run the teardown. There is undoubtedly room for improvement.

* With `pytest-xdist`: I haven't come up with a failing case yet, but it seems like this will be sketchy with tests running in parallel.

* With `pytest-repeat`: This actually works great with `pytest-repeat`, as repeat works by generating parametrized tests.

## FAQ

### Why not just use existing fixture scopes?

There isn't a scope that quite fits.

* Function: runs setup before and after each parametrized test case.
* Class: Kinda works if you put only one function in a test class.
* Module: Too wide.
* Session: Way too wide.

I want a setup that runs before all parametrized test cases, and clean up after the last one.

### Why implement this as a plugin and not add this functionality to pytest core?

A couple reasons.

1. I'm not sure we want this funcitonality in core pytest. Playing with it as a plugin will tell us if it's important to people.
2. Implementing it as a plugin is faster to get it out there and usable.


## Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/).

## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "pytest-param-scope" is free and open source software

## Issues

If you encounter any problems, please [file an issue](https://github.com/okken/pytest-param-scope/issues) along with a detailed description.

## Changelog

See [changelog.md](https://github.com/okken/pytest-param-scope/blob/main/changelog.md)
