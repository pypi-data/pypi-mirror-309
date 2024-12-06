import traceback
import time
from airflow.providers.cncf.kubernetes.operators.custom_object_launcher import CustomObjectLauncher
from airflow.exceptions import AirflowException

class ALCustomObjectLauncher(CustomObjectLauncher):
    def check_pod_start_failure(self):
        try:
            while True:
                pod_status = self.pod_manager.read_pod(self.pod_spec).status
                container_statuses = pod_status.container_statuses

                if container_statuses is None or len(container_statuses) == 0:
                    # Container statuses are not yet available, continue checking
                    print("Waiting for container statuses to be available...")
                    time.sleep(10)
                    continue

                waiting_status = container_statuses[0].state.waiting
                if waiting_status is None:
                    break

                elif waiting_status.reason in ("ContainerCreating", "PodInitializing"):
                    print("---------PodInitializing---------")
                    time.sleep(10)
                else:
                    raise AirflowException(f"Spark Job Failed. Status: {waiting_status.reason}, Error: {waiting_status.message}")
            
        except Exception:
            traceback.print_exc()
            return
