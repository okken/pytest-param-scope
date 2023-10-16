
def test_error_during_setup(pytester):
    pytester.copy_example("examples/test_yield.py")
    result = pytester.runpytest('-v', '-s')
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