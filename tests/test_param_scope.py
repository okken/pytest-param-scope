def test_param(pytester):
    """
    Make sure stuff happens in the right order.
    The test names come from the -v flag.
    The "param setup" looks like it happens after the first test,
    but it doesn't, it's just associated with the beginning of the first test.
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest('test_param_scope.py::test_param', '-v', '-s')
    result.stdout.re_match_lines(
        [
            ".*test_param[[]a[]] .*",
            "param setup",
            ".*test_param[[]b[]] .*",
            ".*test_param[[]c[]] .*",
            "param teardown",
        ],
    )
    result.assert_outcomes(passed=3)


def test_class(pytester):
    """
    Make sure setup and teardown happen for each method.
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest('test_param_scope.py::TestClass', '-v', '-s')
    result.stdout.re_match_lines(
        [
            ".*test_method_1.a.*",
            "param setup",
            ".*test_method_1.b.*",
            ".*test_method_1.c.*",
            "param teardown",

            ".*test_method_2.a.*",
            "param setup",
            ".*test_method_2.b.*",
            ".*test_method_2.c.*",
            "param teardown",

        ],
    )
    result.assert_outcomes(passed=6)


def test_no_param(pytester):
    """
    Make sure setup/teardown happen even if there are no parameters
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest('test_param_scope.py::test_no_param', '-v', '-s')
    result.stdout.fnmatch_lines(
        [
            "param setup",
            "param teardown",
        ],
    )
    result.assert_outcomes(passed=1)



def test_no_setup(pytester):
    """
    Make sure no setup happens, but teardown does.
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest('test_param_scope.py::test_no_setup', '-v', '-s')
    result.stdout.no_fnmatch_line("param setup")
    result.stdout.re_match_lines(
        [
            ".*test_no_setup.a.*",
            ".*test_no_setup.b.*",
            ".*test_no_setup.c.*",
            "param teardown",
        ],
    )
    result.assert_outcomes(passed=3)


def test_no_teardown(pytester):
    """
    Make sure setup happens, but not teardown.
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest('test_param_scope.py::test_no_teardown', '-v', '-s')
    result.stdout.no_fnmatch_line("param teardown")
    result.stdout.re_match_lines(
        [
            ".*test_no_teardown.a.*",
            "param setup",
            ".*test_no_teardown.b.*",
            ".*test_no_teardown.c.*",
        ],
    )
    result.assert_outcomes(passed=3)


def test_no_setup_nor_teardown(pytester):
    """
    Make sure setup happens, but not teardown.
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest(
        'test_param_scope.py::test_no_setup_nor_teardown', '-v', '-s')
    result.stdout.no_fnmatch_line("param setup")
    result.stdout.no_fnmatch_line("param teardown")
    result.stdout.re_match_lines(
        [
            ".*test_no_setup_nor_teardown.a.*",
            ".*test_no_setup_nor_teardown.b.*",
            ".*test_no_setup_nor_teardown.c.*",
        ],
    )
    result.assert_outcomes(passed=3)


def test_no_param_no_mark(pytester):
    """
    Make sure normal tests work fine
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest(
        'test_param_scope.py::test_no_param_no_mark', '-v', '-s')
    result.assert_outcomes(passed=1)


def test_fixture_but_no_mark(pytester):
    """
    Make sure fixture without mark should be a no-op
    """
    pytester.copy_example("examples/test_param_scope.py")
    result = pytester.runpytest(
        'test_param_scope.py::test_fixture_but_no_mark', '-v', '-s')
    result.assert_outcomes(passed=1)
