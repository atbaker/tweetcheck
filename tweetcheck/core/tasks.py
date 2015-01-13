from boto import sns
from celery import shared_task
from django.conf import settings

import json

@shared_task
def send_push_notifications(body, org_id, last_editor_id):
    """Sends SNS push notifications to an org's devices"""
    from core.models import TweetCheckUser, Device
    from twitter.models import Tweet

    last_editor = TweetCheckUser.objects.get(pk=last_editor_id)
    arn_list = Device.objects.filter(user__organization__id=org_id).exclude(user=last_editor) \
        .values_list('arn', flat=True)

    conn = sns.connect_to_region('us-east-1')

    if len(body) > 35:
        body = body[:35].rsplit(' ', 1)[0]+'...'

    alert = '{0} added a new tweet for review: "{1}"'.format(last_editor, body)
    message = {
        'aps': {
            'alert': alert,
            'badge': Tweet.get_pending_count(org_id),
            'sound': 'default'
        }
    }
    sns_request = {settings.SNS_APPLICATION: json.dumps(message)}

    for arn in arn_list:
        conn.publish(message=json.dumps(sns_request),
            message_structure='json',
            target_arn=arn)
