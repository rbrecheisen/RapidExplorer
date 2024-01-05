import time

from tasks.task import Task


class DummyTask(Task):
    def __init__(self) -> None:
        super(DummyTask, self).__init__(name='DummyTask')

    def start(self) -> None:
        self.setStatus(status=Task.IDLE)
        #
        # Re-initialize task if necesesary
        #
        self.setStatus(status=Task.START)
        print('Running dummy task (takes about 5 seconds)...')
        canceled = False        
        for i in range(10):
            print(f'Iteration: {i}')
            if self.status() == Task.CANCELLING:
                print('Cancelling task...')
                canceled = True
                break
            time.sleep(1)
        if canceled:
            self.setStatus(status=Task.CANCELED)
            print('Task canceled')
        else:
            self.setStatus(status=Task.FINISHED)
            print('Task finished')

    def cancel(self) -> None:
        self.setStatus(status=Task.CANCELLING)