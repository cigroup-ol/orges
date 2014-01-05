"""
Tests for the pluggable invoker.
"""
from __future__ import division, print_function, with_statement

from time import sleep

from mock import Mock

from orges.core.args import ArgsCreator
from orges.core.paramspec import ParamSpec
from orges.plugins.timeout import TimeoutPlugin
from orges.invoker.pluggable import PluggableInvoker
from orges.invoker.multithread import MultiThreadInvoker

FUNCTION_SLEEP = 2
INVOKER_TIMEOUT = 1


def f(a, b):
    sleep(FUNCTION_SLEEP)
    return a + b


PARAM_SPEC = ParamSpec()
PARAM_SPEC.int("a", interval=(1, 10))
PARAM_SPEC.int("b", interval=(1, 10))

ARGS = ArgsCreator(PARAM_SPEC).args()


def test():  # TODO: Find some better name for these kind of tests
    simple_invoker = MultiThreadInvoker()

    plugins = [TimeoutPlugin(INVOKER_TIMEOUT)]
    invoker = PluggableInvoker(simple_invoker, plugins=plugins)

    caller = Mock()

    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker.caller = caller
    invoker.invoke(f, ARGS)
    invoker.wait()

    caller.on_result.assert_not_called()
    caller.on_error.assert_called_with(ARGS)

if __name__ == '__main__':
    import nose
    nose.runmodule()