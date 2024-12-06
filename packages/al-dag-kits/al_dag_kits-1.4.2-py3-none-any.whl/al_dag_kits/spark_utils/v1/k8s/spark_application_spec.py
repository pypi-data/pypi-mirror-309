"""
This module defines the SparkApplicationSpec class.
"""

import yaml
import json

from dataclasses import dataclass


@dataclass
class SparkApplicationSpec:

    def __init__(self, task_id, job_yaml, deferrable=False, mode="reschedule"):
        self.task_id = task_id
        self.job_yaml = job_yaml
        self.deferrable = deferrable
        self.mode = mode

        self.job_json = json.loads(json.dumps(yaml.safe_load(self.job_yaml)))