import asyncio
import traceback

from datetime import datetime
from typing import AsyncIterator, Any
from enum import Enum
from kubernetes_asyncio import client

from airflow.exceptions import AirflowException
from airflow.providers.cncf.kubernetes.triggers.pod import KubernetesPodTrigger
from airflow.triggers.base import TriggerEvent
from airflow.utils.session import provide_session
from airflow.models import TaskInstance
from airflow.utils.state import TaskInstanceState
from airflow.settings import Session
from airflow.providers.cncf.kubernetes.utils.pod_manager import PodLaunchTimeoutException

class ContainerState(str, Enum):
    """
    Possible container states.

    See https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase.
    """

    WAITING = "waiting"
    RUNNING = "running"
    TERMINATED = "terminated"
    FAILED = "failed"
    UNDEFINED = "undefined"

class ALKubernetesPodTrigger(KubernetesPodTrigger):
    def __init__(
        self,
        pod_name: str,
        pod_namespace: str,
        trigger_start_time: datetime,
        base_container_name: str,
        kubernetes_conn_id: str = None,
        poll_interval: float = 5,
        cluster_context: str = None,
        in_cluster: bool = None,
        get_logs: bool = True,
        startup_timeout: int = 300,
        startup_check_interval: int = 5,
        on_finish_action: str = "delete_pod",
        last_log_time: datetime = None,
        logging_interval: int = None,
        task_id: str = None,
        dag_id: str = None,
        run_id: str = None,
        map_index: int = 0,
        job_id: int = 0
    ):
        super().__init__(
            pod_name=pod_name,
            pod_namespace=pod_namespace,
            trigger_start_time=trigger_start_time,
            base_container_name=base_container_name,
            kubernetes_conn_id=kubernetes_conn_id,
            poll_interval=poll_interval,
            cluster_context=cluster_context,
            in_cluster=in_cluster,
            get_logs=get_logs,
            startup_timeout=startup_timeout,
            startup_check_interval=startup_check_interval,
            on_finish_action=on_finish_action,
            last_log_time=last_log_time,
            logging_interval=logging_interval,
        )
        self.task_id = task_id
        self.dag_id = dag_id
        self.run_id = run_id
        self.map_index = map_index
        self.job_id = job_id


    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            "al_dag_kits.spark_utils.v1.k8s.al_kubernetes_pod_trigger.ALKubernetesPodTrigger",
            {
                "pod_name": self.pod_name,
                "pod_namespace": self.pod_namespace,
                "trigger_start_time": self.trigger_start_time,
                "base_container_name": self.base_container_name,
                "kubernetes_conn_id": self.kubernetes_conn_id,
                "poll_interval": self.poll_interval,
                "cluster_context": self.cluster_context,
                "in_cluster": self.in_cluster,
                "get_logs": self.get_logs,
                "startup_timeout": self.startup_timeout,
                "startup_check_interval": self.startup_check_interval,
                "on_finish_action": self.on_finish_action,
                "last_log_time": self.last_log_time,
                "logging_interval": self.logging_interval,
                "task_id": self.task_id,
                "dag_id": self.dag_id,
                "run_id": self.run_id,
                "map_index": self.map_index,
                "job_id": self.job_id
            },
        )
    @provide_session
    def get_task_instance(self, session: Session) -> TaskInstance:
        """Retrieve the TaskInstance from the Airflow database."""
        query = session.query(TaskInstance).filter(
            TaskInstance.dag_id == self.dag_id,
            TaskInstance.task_id == self.task_id,
            TaskInstance.run_id == self.run_id,
            TaskInstance.map_index == self.map_index,
        )
        task_instance = query.one_or_none()
        if task_instance is None:
            raise AirflowException(
                f"TaskInstance with dag_id={self.dag_id}, task_id={self.task_id}, "
                f"run_id={self.run_id}, map_index={self.map_index} not found"
            )
        return task_instance

    def safe_to_cancel(self) -> bool:
        """Determine if it's safe to cancel the Kubernetes pod."""
        task_instance = self.get_task_instance()

        if int(task_instance.job_id) != int(self.job_id):
            return True

        return task_instance.state != TaskInstanceState.DEFERRED
    
    # async def _wait_for_container_completion(self) -> TriggerEvent:
    #     """
    #     Wait for container completion.

    #     Waits until container is no longer in running state.
    #     """
    #     while True:
    #         pod = await self.hook.get_pod(self.pod_name, self.pod_namespace)
    #         container_state = self.define_container_state(pod)
    #         if container_state == ContainerState.TERMINATED:
    #             return TriggerEvent(
    #                 {
    #                     "status": "success",
    #                     "namespace": self.pod_namespace,
    #                     "name": self.pod_name,
    #                     "last_log_time": self.last_log_time,
    #                 }
    #             )
    #         elif container_state == ContainerState.FAILED:
    #             return TriggerEvent(
    #                 {
    #                     "status": "failed",
    #                     "namespace": self.pod_namespace,
    #                     "name": self.pod_name,
    #                     "message": "Container state failed",
    #                     "last_log_time": self.last_log_time,
    #                 }
    #             )
    #         self.log.debug("Container is not completed and still working.")
    #         self.log.debug("Sleeping for %s seconds.", self.poll_interval)
    #         await asyncio.sleep(self.poll_interval)

    async def run(self) -> AsyncIterator[TriggerEvent]:
        self.log.info("ALKubernetesPodTrigger starting")
        try:
            state = await self._wait_for_pod_start()
            if state == ContainerState.TERMINATED:
                event = TriggerEvent(
                    {
                        "status": "success",
                        "namespace": self.pod_namespace,
                        "name": self.pod_name,
                        "message": "All containers inside pod have started successfully.",
                    }
                )
            elif state == ContainerState.FAILED:
                event = TriggerEvent(
                    {
                        "status": "failed",
                        "namespace": self.pod_namespace,
                        "name": self.pod_name,
                        "message": "pod failed",
                    }
                )
            else:
                event = await self._wait_for_container_completion()
            yield event
            return

        except PodLaunchTimeoutException as e:
            message = self._format_exception_description(e)
            yield TriggerEvent(
                {
                    "name": self.pod_name,
                    "namespace": self.pod_namespace,
                    "status": "timeout",
                    "message": message,
                }
            )
            return

        except asyncio.CancelledError:
            self.log.info("asyncio.CancelledError was called for ALKubernetesPodTrigger")
            if self.safe_to_cancel():
                self.log.warning("Cancelling Kubernetes pod due to task cancellation.")
                await self._delete_spark_application()
                yield TriggerEvent({"status": "cancelled"})
            else:
                self.log.warning("Triggerer likely stopped, not cancelling Kubernetes pod")

        except Exception as e:
            self.log.exception("Exception occurred while monitoring Kubernetes pod")
            yield TriggerEvent(
                {
                    "name": self.pod_name,
                    "namespace": self.pod_namespace,
                    "status": "error",
                    "message": str(e),
                    "stack_trace": traceback.format_exc(),
                }
            )
            return

    async def _delete_pod(self):
        """Deletes the Kubernetes pod."""
        self.log.info("Deleting pod: %s in namespace: %s", self.pod_name, self.pod_namespace)
        try:
            await self.hook.delete_pod(self.pod_name, self.pod_namespace)
            self.log.info("Pod %s deleted.", self.pod_name)
        except Exception as e:
            self.log.error("Failed to delete Kubernetes pod: %s", e)


    async def _delete_spark_application(self):
        """Deletes the entire Spark application."""
        self.log.info("7 _delete_spark_application() Deleting Spark application associated with pod: %s in namespace: %s", self.pod_name, self.pod_namespace)
        try:
            # pod name includes -driver suffix
            spark_app_name = self.pod_name.replace("-driver", "")
            self.log.info(f"{spark_app_name=}")

            
            async with self.hook.get_conn() as api_client:
                self.log.info(f"{api_client=}")

                # Instantiate the CustomObjectsApi using the API client
                custom_obj_api = client.CustomObjectsApi(api_client)
                self.log.info(f"{custom_obj_api=}")
                
                # we need to call k8s delete api here because this API is not awaited in CustomObjectLauncher
                group = "sparkoperator.k8s.io"
                version = "v1beta2"
                namespace = self.pod_namespace
                plural = "sparkapplications"
                name = spark_app_name

                self.log.info("Delete Spark application: %s", name)

                delete_response = await custom_obj_api.delete_namespaced_custom_object(
                    group=group,
                    version=version,
                    namespace=namespace,
                    plural=plural,
                    name=name,
                    grace_period_seconds=0,
                    propagation_policy="Foreground",
                    async_req=False  # Set to False for synchronous behavior
                )
                
                self.log.info("Spark application %s deleted. delete response = %s", spark_app_name, delete_response)
        except Exception as e:
            traceback.print_exc()
            self.log.error("Failed to delete Spark application: %s", e)
