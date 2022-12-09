import yaml
from aws_cdk import (   
    Stack,
)
from constructs import Construct
from ha_scalablecollector_agent.cloudmap_components.private_namespace_creation import private_namespace_create
from ha_scalablecollector_agent.ecs_components.otel_service import configure_otel_service
from ha_scalablecollector_agent.telemetry_components.prometheus_creation import promethus_endpoint_creation
from ha_scalablecollector_agent.util_components.ssm_parameters_store import configure_ssm_parameters

from ha_scalablecollector_agent.vpc_components.ha_scalablecollector_retrieve_vpc import retrieve_vpc
from ha_scalablecollector_agent.ecs_components.otel_cluster import otel_cluster_create


class HaScalablecollectorAgentStack(Stack):
    


    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SERVICE_NAME = "otel-service"

        # Retrieve VPC information
        vpc = retrieve_vpc(self,"vpc-112233445566"
                                  )

        # Create Otel ECS Cluster
        otel_cluster = otel_cluster_create(self,vpc,SERVICE_NAME)

        # Private DNS Namespace Creation
        privatednsnamespace = private_namespace_create(self,vpc,"otelservice.local")

        # ECS Otel Service Creation

        # 1. Prometheus Endpoint
        # Prometheus Endpoint creation

        prometheus_end_point = promethus_endpoint_creation(self)

        # 2. Configure the Otel-Config Endpoint in Yaml Format
        with open("otel-config.yaml", "r") as stream:
            try:
                aot_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        aot_config["exporters"]["prometheusremotewrite"]["endpoint"] = prometheus_end_point.attr_prometheus_endpoint+"api/v1/remote_write"

        # 3. Create SSM Config Parameter
        ssm_config_param = configure_ssm_parameters(self,"/aot/config/otelservice",aot_config)

        # 4. Otel Service
        configure_otel_service(self,vpc,SERVICE_NAME,otel_cluster,privatednsnamespace,ssm_config_param)
        