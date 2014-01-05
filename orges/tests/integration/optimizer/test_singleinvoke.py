"""
TODO document me
"""
from __future__ import division, print_function, with_statement

from orges.tests.integration.invoker.util import EqualityMatcher as Matcher

from mock import Mock

from orges.core import param
from orges.core.args import ArgsCreator
from orges.invoker.singleprocess import SingleProcessInvoker
from orges.optimizer.singleinvoke import SingleInvokeOptimizer


@param.int("a", interval=(2, 2))
@param.int("b", interval=(1, 1))
def f(a, b):
    return -(a + b)

ARGS = ArgsCreator(f.param_spec).args()


def test_optimize_returns_result():
    caller = Mock()
    caller.on_result = Mock()
    caller.on_error = Mock()

    invoker = SingleProcessInvoker()
    optimizer = SingleInvokeOptimizer()

    optimizer.invoker = invoker
    optimizer.invoker.caller = caller

    optimizer.optimize(f, f.param_spec, None)

    assert not invoker.caller.on_error.called
    invoker.caller.on_result.assert_called_with(Matcher(-3), Matcher(ARGS), {})

if __name__ == '__main__':
    import nose
    nose.runmodule()