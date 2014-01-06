"""
Invoker that can be stopped.
"""
from __future__ import division, print_function, with_statement

from orges.core.args import call
from orges.invoker.base import BaseInvoker
from orges.util.stoppable import Stoppable, stoppable_method

# TODO make this thread-safe


class StoppableInvoker(Stoppable, BaseInvoker):
    """Invoker that can be stopped."""

    def __init__(self):
        super(StoppableInvoker, self).__init__()

    @stoppable_method
    def invoke(self, f, fargs, **kwargs):
        call(f, fargs, **kwargs)

    def wait(self):
        pass