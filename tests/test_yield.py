
def test_yield(pytester):
    pytester.copy_example("examples/test_yield.py")
    result = pytester.runpytest('test_yield.py::test_yield', '-v', '-s')
    result.assert_outcomes(passed=3)
    result.stdout.re_match_lines(
        [
            ".*test_yield.a.*",
            "setup",
            ".*test_yield.b.*",
            ".*test_yield.c.*",
            "teardown",
        ]
    )

def test_two_teardowns(pytester):
    pytester.copy_example("examples/test_yield.py")
    result = pytester.runpytest('test_yield.py::test_two_teardowns', '-v', '-s')
    result.assert_outcomes(passed=3)
    result.stdout.re_match_lines(
        [
            ".*test_two_teardowns.a.*",
            "setup",
            ".*test_two_teardowns.b.*",
            ".*test_two_teardowns.c.*",
            "teardown",
            "separate teardown",
        ]
    )

def test_one_param(pytester):
    pytester.copy_example("examples/test_yield.py")
    result = pytester.runpytest('test_yield.py::test_just_one_func', '-v', '-s')
    result.assert_outcomes(passed=3)
    result.stdout.re_match_lines(
        [
            ".*test_just_one_func.a.*",
            "setup",
            ".*test_just_one_func.b.*",
            ".*test_just_one_func.c.*",
            "teardown",
        ]
    )


def test_no_params(pytester):
    pytester.copy_example("examples/test_yield.py")
    result = pytester.runpytest('test_yield.py::test_no_param_scope_args', '-v', '-s')
    result.assert_outcomes(passed=3)
    result.stdout.re_match_lines(
        [
            ".*test_no_param_scope_args.a.*",
            ".*test_no_param_scope_args.b.*",
            ".*test_no_param_scope_args.c.*",
        ]
    )
