#!/usr/bin/env python3
import datetime
from typing import TYPE_CHECKING

from airflow.utils.context import Context
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.operators.custom_object_launcher import CustomObjectLauncher
from airflow.providers.cncf.kubernetes.callbacks import ExecutionMode
from al_dag_kits.spark_utils.v1.k8s.al_custom_object_launcher import ALCustomObjectLauncher
from al_dag_kits.spark_utils.v1.k8s.al_kubernetes_pod_trigger import ALKubernetesPodTrigger

class ALSparkKubernetesOperator(SparkKubernetesOperator):
    def __init__(self, override_name, **kwargs) -> None:
        self.override_name = override_name 
        super().__init__(**kwargs)  

    def create_job_name(self):
        return self.override_name

    def process_pod_deletion(self, pod, *, reraise=True):
        if pod is not None:
            if self.delete_on_termination:
                self.log.info("Deleting spark job: %s", pod.metadata.name.replace("-driver", ""))
                self.launcher = CustomObjectLauncher(
                    name=self.name,
                    namespace=self.namespace,
                    kube_client=self.client,
                    custom_obj_api=self.custom_obj_api,
                    template_body=self.template_body
                )
                self.launcher.delete_spark_job(pod.metadata.name.replace("-driver", ""))
            else:
                self.log.info("skipping deleting spark job: %s", pod.metadata.name)


    def execute_async(self, context: Context) -> None:
        if self.pod_request_obj is None:
            self.pod_request_obj = self.build_pod_request_obj(context)
        if self.pod is None:
            self.pod = self.get_or_create_pod(  # must set `self.pod` for `on_kill`
                pod_request_obj=self.pod_request_obj,
                context=context,
            )
        if self.callbacks:
            self.callbacks.on_pod_creation(
                pod=self.find_pod(self.pod.metadata.namespace, context=context),
                client=self.client,
                mode=ExecutionMode.SYNC,
            )
        ti = context["ti"]
        ti.xcom_push(key="pod_name", value=self.pod.metadata.name)
        ti.xcom_push(key="pod_namespace", value=self.pod.metadata.namespace)

        self.invoke_defer_method(context)

    def execute(self, context: Context):
        self.log.info("Creating sparkApplication.")
        self.launcher = ALCustomObjectLauncher(
            name=self.name,
            namespace=self.namespace,
            kube_client=self.client,
            custom_obj_api=self.custom_obj_api,
            template_body=self.template_body
        )
        self.pod = self.get_or_create_spark_crd(self.launcher, context)
        self.pod_request_obj = self.launcher.pod_spec

        return super(SparkKubernetesOperator, self).execute(context=context)

    def invoke_defer_method(self, context: Context, last_log_time = None) -> None:
        """Redefine triggers which are being used in child classes."""
        trigger_start_time = datetime.datetime.now(tz=datetime.timezone.utc)
        ti = context["ti"]
        self.defer(
            trigger=ALKubernetesPodTrigger(
                pod_name=self.pod.metadata.name,  # type: ignore[union-attr]
                pod_namespace=self.pod.metadata.namespace,  # type: ignore[union-attr]
                trigger_start_time=trigger_start_time,
                kubernetes_conn_id=self.kubernetes_conn_id,
                cluster_context=self.cluster_context,
                in_cluster=self.in_cluster,
                poll_interval=100,
                get_logs=self.get_logs,
                startup_timeout=1200,
                startup_check_interval=30,
                base_container_name=self.base_container_name,
                on_finish_action=self.on_finish_action.value,
                last_log_time=last_log_time,
                logging_interval=self.logging_interval,
                task_id=ti.task_id,
                dag_id=ti.dag_id,
                run_id=ti.run_id,
                map_index=ti.map_index,
                job_id=ti.job_id
            ),
            method_name="trigger_reentry",
        )
