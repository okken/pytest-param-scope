def test_error_during_setup(pytester):
    """
    Setup exception should cause
    - all tests to error
    - teardown to not run
    """
    pytester.copy_example("examples/test_error.py")
    result = pytester.runpytest('test_error.py::test_error_during_setup', '-v', '-s')
    result.assert_outcomes(errors=3)
    result.stdout.no_fnmatch_line("param teardown")
    result.stdout.re_match_lines(
        [
        "ERROR test_error.py::test_error_during_setup[a] - assert 1 == 2",
        "ERROR test_error.py::test_error_during_setup[b] - assert 1 == 2",
        "ERROR test_error.py::test_error_during_setup[c] - assert 1 == 2",
        ]
    )

def test_error_during_teardown(pytester):
    """
    Teardown exception should cause
    - all tests to pass
    - last test to error
    - yes, this is normal-ish for pytest with parametrized errors.
    """
    pytester.copy_example("examples/test_error.py")
    result = pytester.runpytest('test_error.py::test_error_during_teardown', '-v', '-s')
    result.assert_outcomes(passed=3, errors=1)

