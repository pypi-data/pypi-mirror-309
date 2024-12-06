"""
Utility functions for sending slack messages based off SlackWebhookOperator.
"""

import math
import time
from enum import Enum

from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator


class SlackChannel(Enum):
    """
    Enum of slack channels
    TODO: add more channels as your needed
    """
    SPARK = ('#spark', 'https://hooks.slack.com/services/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')
    ADSERVER = ('#adserver', 'https://hooks.slack.com/services/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')
    ML_ALERTS = ('#ml-alerts', 'https://hooks.slack.com/services/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')
    OPTIMIZER = ('#optimizer', 'https://hooks.slack.com/services/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')
    AIRFLOW_TEST = ('#airflow-test', 'https://hooks.slack.com/services/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')
    MAXWELL_INTERNAL_TOOL = ('#maxwell-internal-tool', 'https://hooks.slack.com/services/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')


class SlackUserGroup(Enum):
    PLATFORMTEAM = '<!subteam^SSHT9D8AU>'


def send_slack(
        context,
        slack_channel=SlackChannel.MAXWELL_INTERNAL_TOOL.value,
        message=f'test msg at {int(math.floor(time.time() * 1000))}',
        username='airflow',
        attachments=None,
        headers=None):
    """
    The job for sending slack msgs to stakeholder and slack rooms via slack web hook.
    """
    channel_name = slack_channel[0]
    webhook_url = slack_channel[1]

    task_slack_alert = SlackWebhookOperator(
        task_id=f'send_slack_{int(math.floor(time.time() * 1000))}',
        username=username,
        http_conn_id=None,
        webhook_token=webhook_url,
        channel=channel_name,
        headers=headers,
        message=message,
        attachments=attachments
    )
    return task_slack_alert.execute(context=context)
