"""
Database that keeps track of worker task relations.
"""
from __future__ import division, print_function, with_statement

from metaopt.invoker.util.model import Start, Error, Result


class TaskWorkerDB():
    """Database that keeps track of worker task relations."""

    def __init__(self, queue_status, queue_outcome):
        self._queue_status = queue_status
        self._queue_outcome = queue_outcome

        self._task_worker_dict = dict()

    def _handle_error(self, error):
        """Handles an error received from the worker via the result queue."""
        print("handle error")  # TODO
        if error.task_id is None:
            # the invoker has closed the queue, so the worker has terminated
            # delete the worker's entry
            print(error)  # TODO
            self._task_worker_dict[error.task_id] = None
        else:
            # an error has occurred in the objective function
            # remove the task's entry
            self._task_worker_dict[error.task_id] = None

    def _handle_result(self, result):
        """Handles a result received from the worker via the result queue."""
        print("handle result")  # TODO
        print(self._task_worker_dict)  # TODO

        if not result.task_id in self._task_worker_dict.keys():
            print(self._task_worker_dict)
            print(self._task_worker_dict.keys())
            print(result.task_id)

            raise KeyError("No task to be stopped for ID %s" % result.task_id)
        if self._task_worker_dict[result.task_id] == None:
            # we got multiple results for the same task
            # that does not make any sense
            raise ValueError("There may be only one result per task." +
                             " Make sure the IDs are unique.")
        self._task_worker_dict[result.task_id] = None

        print(self._task_worker_dict)  # TODO

    def _handle_start(self, start):
        """Handles a start received from the worker via the status queue."""
        print("handle start")  # TODO
        print(self._task_worker_dict)  # TODO

        try:
            if self._task_worker_dict[start.task_id] == start.worker_id:
                # we got the same start repeatedly
                # that does not make any sense
                raise ValueError("Tasks may not be issued repeatedly." +
                             " Make sure the IDs are unique.")
        except KeyError:
            # we could not find the task id in the database
            # that is OK, moving on
            pass

        self._task_worker_dict[start.task_id] = start.worker_id

        print(self._task_worker_dict)  # TODO

    def _handle_finish(self, finish):
        """Handles a finish received from the worker via the status queue."""
        print("handle finish")  # TODO
        print(self._task_worker_dict)  # TODO

        try:
            if self._task_worker_dict[finish.task_id] == None:
                # we got the same start repeatedly
                # that does not make any sense
                raise ValueError("Tasks may not be issued repeatedly." +
                             " Make sure the IDs are unique.")
        except KeyError:
            # we could not find the task id in the database
            # that is OK, moving on
            pass

        # remove done task
        if self._task_worker_dict[finish.task_id] == finish.worker_id:
            # always true
            self._task_worker_dict[finish.task_id] = None
        else:
            # wont happen
            # Another start has occurred in the mean time.
            # The dictionary entry is already up to date.
            # Do nothing.
            pass

        print(self._task_worker_dict)  # TODO

    def wait_for_one_outcome(self):
        """
        Blocks till one Error or one Result was gotten from the outcome queue
        and processed.
        """
        print("wait for one outcome")
        outcome = self._queue_outcome.get()
        print(outcome)  # TODO

        # handle successful results
        if isinstance(outcome, Result):
            print("Result.")  # TODO
            self._handle_result(result=outcome)
            return outcome

        # handle error results
        elif isinstance(outcome, Error):
            print("Error.")  # TODO
            self._handle_error(error=outcome)
            return outcome

        raise TypeError("%s objects are not allowed in the result queue" %
                            type(outcome))

    def wait_for_one_status(self):
        """
        Blocks till one status was gotten from the status queue and processed.
        """
        print("wait for one status")  # TODO

        status = self._queue_status.get()
        print(status)
        if isinstance(status, Start):
            self._handle_start(start=status)
            print("returning start status")
            return status
        raise TypeError("%s objects are not allowed in the status queue" %
                        type(status))

    def wait_for_one_start(self):
        """
        Blocks till one start was gotten from the status queue and processed.
        """
        print("wait for one start")  # TODO
        while True:
            status = self.wait_for_one_status()
            if isinstance(status, Start):
                # a worker started a task
                # so we are done
                break

    def count_running_tasks(self):
        """Returns the number of tasks currently executed by workers."""
        # alternate formulation
        #while len([task for task in self._task_worker_dict.values() if task is not None]) > 0:

        count = 0
        for worker_id in self._task_worker_dict.values():
            if worker_id is not None:
                count += 1
        return count

    def get_worker_id(self, task_id):
        return self._task_worker_dict[task_id]