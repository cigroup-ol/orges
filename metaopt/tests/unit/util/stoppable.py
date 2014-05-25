# -*- coding: utf-8 -*-
"""
Tests for the stoppable.
"""

# Future
from __future__ import absolute_import, division, print_function, \
    unicode_literals, with_statement

# Third Party
import nose
from nose.tools.nontrivial import raises

# First Party
from metaopt.core.stoppable.stoppable import Stoppable
from metaopt.core.stoppable.util.exception import StoppedError
from metaopt.core.stoppable.util.decorator import stoppable


def test_stoppable_is_not_stopped_initially():
    stoppable = Stoppable()
    assert not stoppable.stopped


def test_stopping_is_itempotent():
    stoppable = Stoppable()
    assert not stoppable.stopped
    assert not stoppable.stopped


@raises(StoppedError)
def test_stopping_twice_raises_exception():
    stoppable = Stoppable()
    stoppable.stop()
    stoppable.stop()


def test_stoppablity():
    stoppable = Stoppable()
    stoppable.stop()
    assert stoppable.stopped


def test_stopping_is_idempotent():
    stoppable = Stoppable()
    stoppable.stop()
    assert stoppable.stopped
    assert stoppable.stopped


class MockStoppable(Stoppable):
    """Mock up Stoppable with a stoppable method."""

    @stoppable
    def run(self):
        """A method that does something."""
        pass  # no operation qualifies as "something"


def test_stoppable_decorator():
    mock_stoppable = MockStoppable()
    assert not mock_stoppable.stopped
    mock_stoppable.run()
    mock_stoppable.run()
    mock_stoppable.stop()
    assert mock_stoppable.stopped


@raises(StoppedError)
def test_stoppable_decorator_raises_exception_when_called_after_stopping():
    mock_stoppable = MockStoppable()
    mock_stoppable.run()
    mock_stoppable.run()
    mock_stoppable.stop()
    assert mock_stoppable.stopped
    mock_stoppable.run()

if __name__ == '__main__':
    nose.runmodule()
