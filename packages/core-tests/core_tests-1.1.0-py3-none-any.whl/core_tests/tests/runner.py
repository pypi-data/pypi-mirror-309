# -*- coding: utf-8 -*-

import logging
import os
from sys import exit
from unittest import TestLoader, TextTestRunner

from click import option
from click.decorators import group
from coverage import coverage, CoverageException


@group()
def cli_tests():
    pass


@cli_tests.command("run-tests")
@option("-t", "--test-type", "test_type", default="unit")
def test(test_type: str):
    """ Runs the tests """

    types_ = ["integration", "unit"]
    if test_type not in types_:
        print(f"Wrong test type! Available values: {types_}")
        exit(1)

    if test_type == "unit":
        # Just removing verbosity from unit tests...
        os.environ["LOGGER_LEVEL"] = str(os.getenv("LOGGER_LEVEL_FOR_TEST", logging.ERROR))

    tests = TestLoader().discover(f"./tests/{test_type}", pattern="tests*.py")
    result = TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        exit(1)


@cli_tests.command("run-coverage")
@option("-s", "--save-report", "save_report", default=True)
def cov(save_report: bool = True):
    """ Runs the unit tests and generates a coverage report on success """

    os.environ["LOGGER_LEVEL"] = str(os.getenv("LOGGER_LEVEL_FOR_TEST", logging.ERROR))
    coverage_ = coverage(branch=True, source=["."])
    coverage_.start()

    tests = TestLoader().discover("./tests", pattern="tests*.py")
    result = TextTestRunner(verbosity=2).run(tests)
    coverage_.stop()

    if not result.wasSuccessful():
        exit(1)

    try:
        print("Coverage Summary:")
        coverage_.report()

        if save_report:
            coverage_.save()
            coverage_.html_report()

        coverage_.erase()

    except CoverageException as error:
        print(error)
        exit(1)
