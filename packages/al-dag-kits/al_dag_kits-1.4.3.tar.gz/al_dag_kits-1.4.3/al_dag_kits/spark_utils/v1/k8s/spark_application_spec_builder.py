"""
This is a builder class to build SparkApplicationSpec object with spark job configs in yaml and json formats.
Pass in the required parameters (in string and json formats) and call build() to get the SparkApplicationSpec object.
"""

import yaml
import json
from datetime import datetime

from al_dag_kits.spark_utils.v1.k8s.spark_application_spec import SparkApplicationSpec
from al_dag_kits.spark_utils.v1.k8s.al_cluster_tolerations import parse_tolerations, ClusterType, ClusterSize

class SparkApplicationSpecBuilder:
    def __init__(self):
        self.task_id = f"demo_task_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%03f')}"
        self.yaml_metadata_name = "maxwell-airflow-demo-job"
        self.yaml_metadata_namespace = "spark"
        self.yaml_spec_main_class = "com.applovin.spark.utils.jobs.SparkJobRunner"
        self.yaml_spec_main_application_file = "gs://applovin-hdfs-us-east1/deploys/sparkjobs/network_comparison_auto_cpm_job.jar"
        self.yaml_spec_job_class = "com.applovin.spark.jobserver.jobs.HelloWorld"
        self.yaml_spec = None
        self.yaml_spec_arguments = None
        self.yaml_spec_mode = None
        self.yaml_spec_image = None
        self.yaml_spec_dynamic_allocation = None
        self.yaml_spec_volumes = None
        self.yaml_spec_spark_conf = None
        self.yaml_spec_spark_conf_log_dc = "mks"
        self.yaml_spec_driver = None
        self.yaml_spec_driver_env_k8_env = "prod"
        self.yaml_spec_driver_env_region = "us-east1"
        self.yaml_spec__service_account = "mks-aggrok8"
        self.yaml_spec_driver_lifecycle = None
        self.yaml_spec_driver_rpc_producer = True
        self.yaml_spec__node_selector_node_pool = ""
        self.yaml_spec__gcs_project_id = "strategic-atom-700"
        self.yaml_spec_executor = None
        self.yaml_spec_restart_policy = None
        self.yaml_spec_spark_ui_options = {
            "ingressAnnotations": {
                "kubernetes.io/ingress.class": "ingress-controller-internal"
            }
        }
        self.label_version = "3.5.0"
        self.label_app = "spark-gke"
        self.label_team = None
        self.label_env = None
        self.label_region = None
        self.label_dc = None
        self.label_spark_app = None
        self.yaml_spec_hadoop_fs_default_fs = None
        self.yaml_spec_hadoop_conf = None
        self.yaml_spec_hadoop_conf_override = False
        self.use_pv = True
        self.pv_size = None
        self.pv_type = None
        self.yaml_spec_tolerations = [
            {
                "effect": "NoSchedule",
                "key": ClusterType.DEDICATED.value,
                "value": "true",
            },
            {
                "key": "size",
                "value": ClusterSize.BIG.value,
                "effect": "NoSchedule",
            },
            {
                "key": "size",
                "value": ClusterSize.MEDIUM.value,
                "effect": "NoSchedule",
            },
            {
                "key": "size",
                "value": ClusterSize.SMALL.value,
                "effect": "NoSchedule",
            }
        ]

    def set_task_id(self, task_id):
        self.task_id = task_id
        return self

    def set_yaml_metadata_name(self, yaml_metadata_name):
        self.yaml_metadata_name = yaml_metadata_name
        return self

    def set_yaml_metadata_namespace(self, yaml_metadata_namespace):
        self.yaml_metadata_namespace = yaml_metadata_namespace
        return self

    def set_yaml_spec_dynamic_allocation(self, yaml_spec_dynamic_allocation):
        self.yaml_spec_dynamic_allocation = yaml_spec_dynamic_allocation
        return self

    def set_yaml_spec(self, yaml_spec):
        '''
        Spec params in json format.
        '''
        self.yaml_spec = yaml_spec
        return self

    def set_yaml_spec_mode(self, yaml_spec_mode):
        self.yaml_spec_mode = yaml_spec_mode
        return self

    def set_yaml_spec_image(self, yaml_spec_image):
        self.yaml_spec_image = yaml_spec_image
        return self

    def set_yaml_spec_main_class(self, yaml_spec_main_class):
        self.yaml_spec_main_class = yaml_spec_main_class
        return self

    def set_yaml_spec_main_application_file(self, yaml_spec_main_application_file):
        self.yaml_spec_main_application_file = yaml_spec_main_application_file
        return self

    def set_yaml_spec_job_class(self, yaml_spec_job_class):
        self.yaml_spec_job_class = yaml_spec_job_class
        return self

    def set_yaml_spec_dc(self, yaml_spec_dc):
        self.yaml_spec_job_class = yaml_spec_dc
        return self

    def set_yaml_spec_spark_conf_log_dc(self, yaml_spec_spark_conf_log_dc):
        self.yaml_spec_spark_conf_log_dc = yaml_spec_spark_conf_log_dc
        return self

    def set_yaml_spec_driver_env_k8_env(self, yaml_spec_driver_env_k8_env):
        self.yaml_spec_driver_env_k8_env = yaml_spec_driver_env_k8_env
        return self

    def set_yaml_spec_driver_env_region(self, yaml_spec_driver_env_region):
        self.yaml_spec_driver_env_region = yaml_spec_driver_env_region
        return self

    def set_yaml_spec__service_account(self, yaml_spec_driver_service_account):
        self.yaml_spec__service_account = yaml_spec_driver_service_account
        return self

    def set_yaml_spec_driver_node_selector_node_pool(self, yaml_spec_driver_node_selector_node_pool):
        self.yaml_spec__node_selector_node_pool = yaml_spec_driver_node_selector_node_pool
        return self

    def set_yaml_spec_driver_lifecycle(self, yaml_spec_driver_lifecycle):
        self.yaml_spec_driver_lifecycle = yaml_spec_driver_lifecycle
        return self

    def set_yaml_spec_driver_rpc_producer(self, yaml_spec_driver_rpc_producer=True):
        self.yaml_spec_driver_rpc_producer = yaml_spec_driver_rpc_producer
        return self

    def set_yaml_spec_arguments(self, yaml_spec_arguments):
        self.yaml_spec_arguments = yaml_spec_arguments
        return self

    def set_yaml_spec_volumes(self, yaml_spec_volumes):
        self.yaml_spec_volumes = yaml_spec_volumes
        return self

    def set_yaml_spec_hadoop_conf(self, yaml_spec_hadoop_conf, override = False):
        self.yaml_spec_hadoop_conf = yaml_spec_hadoop_conf
        self.yaml_spec_hadoop_conf_override = override
        return self

    def set_yaml_spec_spark_conf(self, yaml_spec_spark_conf):
        self.yaml_spec_spark_conf = yaml_spec_spark_conf
        return self

    def set_yaml_spec_driver(self, yaml_spec_driver):
        self.yaml_spec_driver = yaml_spec_driver
        return self

    def set_yaml_spec_executor(self, yaml_spec_executor):
        self.yaml_spec_executor = yaml_spec_executor
        return self

    def set_yaml_spec_restart_policy(self, yaml_spec_restart_policy):
        self.yaml_spec_restart_policy = yaml_spec_restart_policy
        return self

    def set_yaml_spec_spark_ui_options(self, yaml_spec_spark_ui_options):
        self.yaml_spec_spark_ui_options = yaml_spec_spark_ui_options
        return self

    def set_label_version(self, label_version):
        self.label_version = label_version
        return self

    def set_label_app(self, label_app):
        self.label_app = label_app
        return self

    def set_label_team(self, label_team):
        self.label_team = label_team
        return self

    def set_label_env(self, label_env):
        self.label_env = label_env
        return self

    def set_label_region(self, label_region):
        self.label_region = label_region
        if self.yaml_spec_hadoop_fs_default_fs == None:
            self.yaml_spec_hadoop_fs_default_fs = f"gs://applovin-hdfs-{self.label_region}"
        return self

    def set_label_dc(self, label_dc):
        self.label_dc = label_dc
        return self
    
    def set_label_spark_app(self, label_spark_app):
        self.label_spark_app = label_spark_app
        return self

    def set_yaml_spec_hadoop_fs_default_fs(self, yaml_spec_hadoop_fs_default_fs):
        '''
        This setter will be overriden if hadoopConf or sparkConf is explicitly set
        '''
        self.yaml_spec_hadoop_fs_default_fs = yaml_spec_hadoop_fs_default_fs
        return self
    
    def set_pv_size(self, pv_size):
        self.pv_size = pv_size
        return self

    def set_pv_type(self, pv_type):
        self.pv_type = pv_type
        return self

    def set_use_pv(self, use_pv):
        self.use_pv = use_pv
        return self
    
    def set_tolerations(self, tolerations: list):
        '''
        Set tolerations for both driver and executor
        
        Input:
        tolerations: list of tolerations, allowed values:  
        - small
        - medium
        - big
        - dedicated
        - spot
        '''
        self.yaml_spec_tolerations = parse_tolerations(tolerations)
        return self
    
    def build(self):
        def get_initcontainer_args():
            return """
            set -e
            echo "Creating necessary directories..."
            mkdir -p /tmp/applovin/sparkjob/ 
            ls -al /tmp/applovin/sparkjob/
            echo "Downloading configuration files..."
            gsutil cp gs://applovin-hdfs-$REGION/configs/applovin/sparkjob/sparkjob.properties /tmp/applovin/sparkjob/ || { echo "Failed to download sparkjob.properties"; exit 1; }
            gsutil cp -r gs://applovin-hdfs-$REGION/sparkjob_k8s_resources/configs/* /tmp/applovin/sparkjob/ || { echo "Failed to download configs"; exit 1; }
            gsutil cp gs://applovin-hdfs-$REGION/sparkjob_k8s_resources/misc/graphitestatslogger.properties /tmp/applovin/sparkjob/graphitestatslogger.properties || { echo "Failed to download graphitestatslogger.properties"; exit 1; }
            gsutil cp gs://applovin-hdfs-$REGION/sparkjob_k8s_resources/misc/log4j2.$K8_ENV.properties /tmp/applovin/sparkjob/log4j2.properties || { echo "Failed to download log4j2.properties"; exit 1; }
            echo "Listing configuration directory contents after download..."
            ls -al /tmp/applovin/sparkjob/
            """
        default_config = {
            "apiVersion": "sparkoperator.k8s.io/v1beta2",
            "kind": "SparkApplication",
            "metadata": {
                "name": self.yaml_metadata_name,
                "namespace": self.yaml_metadata_namespace
            },
            "spec": {
                "type": "Scala",
                "mode": "cluster",
                "image": "gcr.io/high-codex-314318/spark-k8:0.0.2",
                "imagePullPolicy": "Always",
                "mainClass": self.yaml_spec_main_class,
                "mainApplicationFile": self.yaml_spec_main_application_file,
                "sparkVersion": "3.5.0",
                "timeToLiveSeconds": 1000,
                "arguments": [
                    self.yaml_spec_job_class,
                    "driver_sleep=900000"
                ],
                "dynamicAllocation": {
                    "enabled": False,
                    "initialExecutors": 2,
                    "minExecutors": 2,
                    "maxExecutors": 32
                },
                "hadoopConf": {
                    "google.cloud.auth.service.account.enable": "true",
                    "fs.defaultFS": self.yaml_spec_hadoop_fs_default_fs if self.yaml_spec_hadoop_fs_default_fs else f"gs://applovin-hdfs-{self.yaml_spec_driver_env_region}",
                    "spark.hadoop.core:io.compression.codecs": "org.apache.hadoop.io.compress.GzipCodec,org.apache.hadoop.io.compress.DeflateCodec,org.apache.hadoop.io.compress.SnappyCodec,org.apache.hadoop.io.compress.BZip2Codec,org.apache.hadoop.io.compress.Lz4Codec,org.apache.hadoop.io.compress.NewLineConcatGzipCodec"
                },
                "sparkConf": {
                    "hadoop.fs.defaultFS": self.yaml_spec_hadoop_fs_default_fs if self.yaml_spec_hadoop_fs_default_fs else f"gs://applovin-hdfs-{self.yaml_spec_driver_env_region}",
                    "spark.executor.instances": "2",
                    "spark.executor.cores": "16",
                    "spark.executor.memory": "40g",
                    "spark.cores.max": "16",
                    "spark.sql.shuffle.partitions": "4",
                    "spark.default.parallelism": "4",
                    "spark.sql.files.openCostInBytes": "536870912",
                    "spark.sql.files.maxPartitionBytes": "536870912",
                    "spark.reducer.maxSizeInFlight": "1024m",
                    "spark.storage.blockManagerSlaveTimeoutMs": "43200000",
                    "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version": "2",
                    "spark.task.maxFailures": "10",
                    "spark.executor.heartbeatInterval": "300s",
                    "spark.network.timeout": "1200s",
                    "spark.rpc.askTimeout": "600",
                    "spark.driver.memory": "40g",
                    "spark.scheduler.listenerbus.eventqueue.capacity": "10000000",
                    "spark.driver.maxResultSize": "40g",
                    "spark.sql.session.timeZone": "UTC",
                    "spark.eventLog.dir": f"gs://applovin-sparkjob-logs/{self.yaml_spec_spark_conf_log_dc}",
                    "spark.eventLog.enabled": "true",
                    "spark.eventLog.rolling.enabled": "true",
                    "spark.eventLog.rolling.maxFileSize": "128m",
                    "spark.dynamicAllocation.executorIdleTimeout": "600s"
                },
                "sparkUIOptions": {
                    "ingressAnnotations": {
                        "kubernetes.io/ingress.class": "nginx-internal"
                    }
                },
                "driver": {
                    "env": [
                        {
                            "name": "K8_ENV",
                            "value": self.yaml_spec_driver_env_k8_env
                        },
                        {
                            "name": "REGION",
                            "value": self.yaml_spec_driver_env_region
                        },
                        {
                            "name": "HADOOP_CONF_DIR",
                            "value": "/configs/applovin/sparkjob/"
                        }
                    ],
                    "cores": 1,
                    "labels": {
                        "version": self.label_version,
                        "app": self.label_app,
                        "team": self.label_team,
                        "env": self.label_env,
                        "region": self.label_region,
                        "dc": self.label_dc,
                        "spark_app": self.label_spark_app
                    },
                    "serviceAccount": self.yaml_spec__service_account,
                    "nodeSelector": {
                        "node_pool": self.yaml_spec__node_selector_node_pool
                    } if self.yaml_spec__node_selector_node_pool else {},
                    "tolerations": [
                        {
                            "key": self.yaml_spec__node_selector_node_pool,
                            "operator": "Equal",
                            "effect": "NoSchedule",
                            "value": "true"
                        } 
                    ] if self.yaml_spec__node_selector_node_pool else [],
                    "envVars": {
                        "GCS_PROJECT_ID": self.yaml_spec__gcs_project_id
                    },
                    "initContainers": [
                        {
                            "name": "init-config",
                            "image": "google/cloud-sdk:latest",
                            "command": ["/bin/sh", "-c"],
                            "env": [
                                {
                                    "name": "K8_ENV",
                                    "value": self.yaml_spec_driver_env_k8_env
                                },
                                {
                                    "name": "REGION",
                                    "value": self.yaml_spec_driver_env_region
                                }
                            ],
                            "args": [
                                get_initcontainer_args()
                            ],
                            "volumeMounts": [
                                {
                                    "name": "config-volume",
                                    "mountPath": "/tmp/applovin/sparkjob"
                                }
                            ]
                        }
                    ],
                    "volumeMounts": [
                        {
                            "name": "config-volume",
                            "mountPath": "/configs/applovin/sparkjob/"
                        },
                        {
                            "name": "config-volume",
                            "mountPath": "/etc/spark/conf/graphitestatslogger.properties",
                            "subPath": "graphitestatslogger.properties"
                        },
                        {
                            "name": "config-volume",
                            "mountPath": "/etc/spark/conf/log4j2.properties",
                            "subPath": "log4j2.properties"
                        }
                    ]
                },
                "executor": {
                    "env": [
                        {
                            "name": "K8_ENV",
                            "value": self.yaml_spec_driver_env_k8_env
                        },
                        {
                            "name": "REGION",
                            "value": self.yaml_spec_driver_env_region
                        },
                        {
                            "name": "HADOOP_CONF_DIR",
                            "value": "/configs/applovin/sparkjob/"
                        }
                    ],
                    "labels": {
                        "version": self.label_version,
                        "app": self.label_app,
                        "team": self.label_team,
                        "env": self.label_env,
                        "region": self.label_region,
                        "dc": self.label_dc,
                        "spark_app": self.label_spark_app
                    },
                    "serviceAccount": self.yaml_spec__service_account,
                    "nodeSelector": {
                        "node_pool": self.yaml_spec__node_selector_node_pool
                    } if self.yaml_spec__node_selector_node_pool else {},
                    "tolerations": [
                        {
                            "key": self.yaml_spec__node_selector_node_pool,
                            "operator": "Equal",
                            "effect": "NoSchedule",
                            "value": "true"
                        } 
                    ] if self.yaml_spec__node_selector_node_pool else [],
                    "envVars": {
                        "GCS_PROJECT_ID": self.yaml_spec__gcs_project_id
                    },
                    "initContainers": [
                        {
                            "name": "init-config",
                            "image": "google/cloud-sdk:latest",
                            "command": ["/bin/sh", "-c"],
                            "env": [
                                {
                                    "name": "K8_ENV",
                                    "value": self.yaml_spec_driver_env_k8_env
                                },
                                {
                                    "name": "REGION",
                                    "value": self.yaml_spec_driver_env_region
                                }
                            ],
                            "args": [
                                get_initcontainer_args()
                            ],
                            "volumeMounts": [
                                {
                                    "name": "config-volume",
                                    "mountPath": "/tmp/applovin/sparkjob"
                                }
                            ]
                        }
                    ],
                    "volumeMounts": [
                        {
                            "name": "config-volume",
                            "mountPath": "/configs/applovin/sparkjob/"
                        },
                        {
                            "name": "config-volume",
                            "mountPath": "/etc/spark/conf/graphitestatslogger.properties",
                            "subPath": "graphitestatslogger.properties"
                        },
                        {
                            "name": "config-volume",
                            "mountPath": "/etc/spark/conf/log4j2.properties",
                            "subPath": "log4j2.properties"
                        }
                    ],
                },
                "volumes": [
                    {
                        "name": "config-volume",
                        "emptyDir": {}
                    }
                ]
            }
        }

        if self.yaml_spec is not None:
            default_config["spec"].update(self.yaml_spec)

        if self.yaml_spec_arguments is not None:
            default_config["spec"]["arguments"] = self.yaml_spec_arguments

        if self.yaml_spec_mode is not None:
            default_config["spec"]["mode"] = self.yaml_spec_mode

        if self.yaml_spec_image is not None:
            default_config["spec"]["image"] = self.yaml_spec_image

        if self.yaml_spec_dynamic_allocation is not None:
            default_config["spec"]["dynamicAllocation"].update(self.yaml_spec_dynamic_allocation)

        if self.yaml_spec_spark_conf is not None:
            default_config["spec"]["sparkConf"].update(self.yaml_spec_spark_conf)

        if self.yaml_spec_hadoop_conf is not None:
            if self.yaml_spec_hadoop_conf_override:
                default_config["spec"]["hadoopConf"] = self.yaml_spec_hadoop_conf
            else:
                default_config["spec"]["hadoopConf"].update(self.yaml_spec_hadoop_conf)
        else:
            default_config["spec"].pop("hadoopConf", None)
            default_config["spec"]["sparkConf"].pop("hadoop.fs.defaultFS", None)

        if self.yaml_spec_driver is not None:
            default_config["spec"]["driver"].update(self.yaml_spec_driver)

        if self.yaml_spec_executor is not None:
            default_config["spec"]["executor"].update(self.yaml_spec_executor)

        if self.yaml_spec_spark_ui_options is not None:
            default_config["spec"]["sparkUIOptions"].update(self.yaml_spec_spark_ui_options)

        if self.yaml_spec_driver_lifecycle is not None:
            default_config["spec"]["driver"]["lifecycle"].update(self.yaml_spec_driver_lifecycle)

        if not self.yaml_spec_driver_rpc_producer:
            default_config["spec"]["driver"]["lifecycle"]["postStart"]["exec"]["command"] =\
            [
                "/bin/sh",
                "-c",
                "mkdir -p /configs/applovin/sparkjob/ /home/spark/ && "
                "/usr/bin/gsutil cp gs://applovin-hdfs-$REGION/configs/applovin/sparkjob/sparkjob.properties /configs/applovin/sparkjob; "
                "/usr/bin/gsutil cp -r gs://applovin-hdfs-$REGION/sparkjob_k8s_resources/configs/* /configs/applovin/sparkjob/; "
                "/usr/bin/gsutil cp gs://applovin-hdfs-$REGION/sparkjob_k8s_resources/setup_producer_k8s.sh /home/spark/ && /usr/bin/chmod +x /home/spark/setup_producer_k8s.sh;"
                "./setup_producer_k8s.sh;"
            ]

        if self.yaml_spec_restart_policy is not None:
            if default_config["spec"].get("restartPolicy") is None:
                default_config["spec"]["restartPolicy"] = {}
            default_config["spec"]["yaml_spec_restart_policy"].update(self.yaml_spec_restart_policy)

        if self.yaml_spec_volumes is not None:
            if default_config["spec"].get("volumes") is None:
                default_config["spec"]["volumes"] = {}
            default_config["spec"]["volumes"].update(self.yaml_spec_volumes)
            
        if self.yaml_spec_tolerations is not None:
            default_config["spec"]["executor"]["tolerations"] = self.yaml_spec_tolerations
            default_config["spec"]["driver"]["tolerations"] = self.yaml_spec_tolerations

        # Add pv_spec to sparkConf if pv_size or pv_type is specified
        if self.use_pv:
            pvc_prefix = "spark.kubernetes.executor.volumes.persistentVolumeClaim.spark-local-dir-1"
            pv_spec = {
                f"{pvc_prefix}.options.claimName": "OnDemand",
                f"{pvc_prefix}.mount.path": "/var/data/spark",
                f"{pvc_prefix}.mount.readOnly": "false",
                f"{pvc_prefix}.options.storageClass": "ssd" if self.pv_type is None else self.pv_type,
                f"{pvc_prefix}.options.sizeLimit": "100Gi" if self.pv_size is None else self.pv_size,
                "spark.kubernetes.driver.ownPersistentVolumeClaim": "true",
                "spark.kubernetes.driver.reusePersistentVolumeClaim": "true",
                "spark.kubernetes.driver.waitToReusePersistentVolumeClaim": "true"
            }
            default_config["spec"]["executor"]["podSecurityContext"] = {
                "fsGroup": 185,
                "fsGroupChangePolicy": "OnRootMismatch"
            }
            default_config["spec"]["sparkConf"].update(pv_spec)

        return SparkApplicationSpec(task_id=self.task_id, job_yaml=yaml.dump(default_config, default_flow_style=False))
