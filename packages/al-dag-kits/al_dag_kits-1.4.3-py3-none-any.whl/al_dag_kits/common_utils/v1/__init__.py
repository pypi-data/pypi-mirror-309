from airflow.operators.python import get_current_context
from datetime import datetime, timedelta

GROUP_EMAIL = 'business-intelligence-tools@applovin.com'
# TODO: add custom emails
EMAILS = [GROUP_EMAIL]

DEFAULT_ARGS = {
    'owner': GROUP_EMAIL,
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 28),
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    'email': EMAILS,
    'email_on_retry': False,
    'email_on_failure': True,
}

LOAD_JOB_PARAMS_TASK = "load_job_params_task"


def get_context():
    """
    Get current airflow dag context
    """
    return get_current_context()


def pull_xcom(task_ids=LOAD_JOB_PARAMS_TASK):
    """
    Pull xcom from a task in dag
    """
    ti = get_current_context()["ti"]
    print(f"---- ti: {task_ids}: {ti.xcom_pull(task_ids=task_ids)}")
    return ti.xcom_pull(task_ids=task_ids)


def get_xcom_param(task_ids, key, default=None):
    """
    Get xcom param from a task in dag
    """
    return pull_xcom(task_ids=task_ids).get(key, default)


def get_xcom_value_or_default(task_id, key, default_value=None):
    xcom_value = pull_xcom(task_ids=task_id)
    if isinstance(xcom_value, dict):
        return xcom_value.get(key, default_value)
    elif xcom_value is not None:
        return xcom_value
    return default_value
