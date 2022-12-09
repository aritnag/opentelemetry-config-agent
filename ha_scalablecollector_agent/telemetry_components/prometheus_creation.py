import yaml
from aws_cdk import (
    # Duration,
    Duration,
    RemovalPolicy,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_servicediscovery as servicediscovery,
    aws_aps as prometheus,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_logs as logs
    
)

def promethus_endpoint_creation(self):
    return prometheus.CfnWorkspace(self, 'otel-service-workspace',
                                                       alias="otel-service-workspace")

