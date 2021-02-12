import asyncio
import json
import boto3
import re
import requests
import aiobotocore


class Manager:

    def __init__(self, tasks, queue):
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks
        self.queue = queue

    async def _get_messages(self):
        return self.queue.receive_messages()

    async def send_to_sandbox(self, file):
        pass

    async def antivirus_check(self, file):
        pass

    async def main(self):
        print('Listener started')
        while True:
            messages = await self._get_messages()
            for message in messages:
                body = json.loads(message.body)
                body = json.loads(body)

                task_name = body.get('task')
                args = body.get('args', ())
                kwargs = body.get('kwargs', {})

                task = self.tasks.get(task_name)
                self.loop.create_task(task(*args, **kwargs))
                message.delete()
            await asyncio.sleep(1)


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='toDlp')


async def dlp_check_patterns(patterns, file):
    print(f'We are checking patterns in {file}')
    found_patterns = []

    for pattern in patterns:
        if re.search(pattern['content'], file):
            found_patterns.append(pattern)

    print(' === Found patterns ===')
    print(found_patterns)
    print(' === End patterns ===')

    json = {"found_patterns": found_patterns, 'text': file}

    print("Sending request back to Django...")
    requests.post(url='http://app-django:8000/event/entry_hook/', json=json)
    print("Sent!")

tasks = {
    'dlp_check_patterns': dlp_check_patterns,
    'send_to_sandbox': Manager.send_to_sandbox,
    'antivirus_check': Manager.antivirus_check,
}

manager = Manager(tasks, queue)

try:
    manager.loop.run_until_complete(manager.main())
finally:
    manager.loop.close()
