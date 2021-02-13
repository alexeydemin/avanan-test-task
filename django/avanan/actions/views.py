from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import status
from web.models import Pattern, Entry
import json
import boto3
from django.http import HttpResponse, JsonResponse
import requests


def write_to_queue_for_dlp(msg):
    patterns = Pattern.objects.filter(is_active=True)
    patterns = [{'title': pattern.title, 'content': pattern.content} for pattern in patterns]

    sqs = boto3.resource('sqs')
    sqs.create_queue(QueueName='toDlp', Attributes={'DelaySeconds': '3'})
    queue = sqs.get_queue_by_name(QueueName='toDlp')

    blob = msg.encode()

    # Required message format
    body = {
        'task': 'dlp_check_patterns',
        'args': (),
        'kwargs': {'patterns': patterns, 'file': blob.decode("utf-8")}
    }

    serialised_body = json.dumps(body)
    body_str = json.dumps(serialised_body)

    print('\n=== Writing a message to queue === ')
    response = queue.send_message(MessageBody=body_str)
    print(response)
    print('=== End of writing a message to queue ===\n')


def save_entries_to_db(payload):
    problems = payload["found_patterns"]
    text = payload["text"]

    for problem in problems:
        entry = Entry(
            pattern_title=problem["title"],
            pattern_content=problem["content"],
            message=text
        )
        entry.save()


@csrf_exempt
def entry_hook(request):
    json_dict = json.loads(request.body.decode('utf-8'))

    print('\n=== Request from DLP === ')
    print(json_dict)
    print('=== End of request from DLP ===\n')

    print('\n==== Saving bad entries to the DB... ===')
    save_entries_to_db(json_dict)
    print('=== Saved ===\n')

    return HttpResponse(status=status.HTTP_200_OK)


@csrf_exempt
def slack_hook(request):
    json_dict = json.loads(request.body.decode('utf-8'))

    print('\n=== Request from Slack === ')
    print(json_dict)
    print('=== End of request from Slack ===\n ')

    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)

    if 'event' in json_dict:
        event_msg = json_dict['event']

        if 'bot_profile' in event_msg:
            return HttpResponse(status=status.HTTP_200_OK)

        if event_msg['type'] == 'message' and 'X-Slack-Retry-Num' not in request.headers:
            if event_msg['text']:
                write_to_queue_for_dlp(event_msg['text'])
            if 'files' in event_msg:
                for file in event_msg['files']:
                    url = file["url_private"]
                    token = settings.BOT_USER_ACCESS_TOKEN
                    file_text = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
                    print(file_text.text)
                    write_to_queue_for_dlp(file_text.text)

            return HttpResponse(status=status.HTTP_202_ACCEPTED)

    return HttpResponse(status=status.HTTP_200_OK)
