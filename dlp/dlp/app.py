import asyncio
import json
import re
import httpx
import aiobotocore


class Manager:

    def __init__(self, tasks, session):
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks
        self.session = session

    async def _get_messages(self):
        async with session.create_client('sqs', region_name='us-east-1') as client:
            response = await client.create_queue(QueueName='toDlp')
            queue_url = response['QueueUrl']
            sqs_message = await client.receive_message(QueueUrl=queue_url)
            if 'Messages' in sqs_message:
                message = sqs_message['Messages'][0]
                receipt_handle = message['ReceiptHandle']
                del_response = await client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                print('\nDeleting message %s' % message['Body'])
                print(del_response)
                print('Deleted\n')

                return message

    async def send_to_sandbox(self, file):
        pass

    async def antivirus_check(self, file):
        pass

    async def main(self):
        print('Listener started')
        while True:
            message = await self._get_messages()
            if not message:
                continue

            print('\n== message ==')
            print(message)
            print('== message ==\n')

            body = json.loads(message['Body'])

            print('\n== body ==')
            print(body)
            print('== body ==\n')
            body = json.loads(body)

            task_name = body.get('task')
            args = body.get('args', ())
            kwargs = body.get('kwargs', {})

            task = self.tasks.get(task_name)
            self.loop.create_task(task(*args, **kwargs))

            await asyncio.sleep(1)


async def dlp_check_patterns(patterns, file):
    print(f'We are checking patterns in ["{file}"]')
    found_patterns = []

    for pattern in patterns:
        if re.search(pattern['content'], file):
            found_patterns.append(pattern)

    print(' === Found patterns ===')
    print(found_patterns)
    print(' === End patterns ===')

    if found_patterns:
        json_payload = {"found_patterns": found_patterns, 'text': file}
        print("Sending request back to Django...")

        async with httpx.AsyncClient() as client:
            await client.post(url='http://app-django:8000/event/entry_hook/', json=json_payload)
        print("Sent!")


tasks = {
    'dlp_check_patterns': dlp_check_patterns,
    'send_to_sandbox': Manager.send_to_sandbox,
    'antivirus_check': Manager.antivirus_check,
}


session = aiobotocore.get_session()
manager = Manager(tasks, session)

try:
    manager.loop.run_until_complete(manager.main())
finally:
    manager.loop.close()
