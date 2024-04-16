import requests
import json

from mosamaticdesktop.tasks.task import Task
from mosamaticdesktop.logger import Logger

LOGGER = Logger()


class TotalSegmentatorSliceSelectionTask(Task):
    def __init__(self) -> None:
        super(TotalSegmentatorSliceSelectionTask, self).__init__()
        self.addDescriptionParameter(
            name='description',
            description='Uses microservice to automatically select L3 vertebra from list of CT scans in XNAT',
        )
        # self.addTextParameter(
        #     name='projectName',
        #     labelText='Project name in XNAT'
        # )
        # self.addTextParameter(
        #     name='URL',
        #     labelText='URL of XNAT server',
        # )
        # self.addTextParameter(
        #     name='username',
        #     labelText='Username',
        # )
        # self.addTextParameter(
        #     name='password',
        #     labelText='Password',
        # )
        # self.addOptionGroupParameter(
        #     name='vertebra',
        #     labelText='Vertebra to select',
        #     options=[
        #         'L3',
        #         'T4',
        #     ],
        # )

    def execute(self) -> None:
        result = requests.post('http://127.0.0.1:8000/users', headers={
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }, json={
            'username': 'ralph',
            'password_hash': 'somesecretpassword',
            'permission_key': '08a028e2373d2106',
        })
        LOGGER.info(f'{result.reason} ({result.status_code})')