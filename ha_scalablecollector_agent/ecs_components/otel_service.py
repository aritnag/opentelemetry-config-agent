
import yaml
from aws_cdk import (
    # Duration,
    Duration,
    RemovalPolicy,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_servicediscovery as servicediscovery,
    aws_iam as iam,
    aws_logs as logs
    
)
def configure_otel_service(self, vpc,service_name,otel_cluster,privatednsnamespace,config_param):
    
        otel_security_group = ec2.SecurityGroup(self, 'otel-security-group', vpc=vpc,
                                                allow_all_outbound=True)
        otel_security_group.add_ingress_rule(peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
                                             connection=ec2.Port.tcp_range(4317, 4317))
        otel_security_group.add_ingress_rule(peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
                                             connection=ec2.Port.tcp_range(2000, 2000))
        otel_security_group.add_ingress_rule(peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
                                             connection=ec2.Port.tcp_range(8125, 8125))

        # 5. Otel Sevice Role
        otel_service_role = iam.Role(self, 'otel-service-role',
                                     path="/",
                                     assumed_by=iam.ServicePrincipal(
                                         "ecs-tasks.amazonaws.com"),
                                     inline_policies={
                                         'GetConfigParamters': iam.PolicyDocument(
                                             statements=[
                                                 iam.PolicyStatement(
                                                     effect=iam.Effect.ALLOW,
                                                     actions=["ssm:GetParameter",
                                                              "ssm:GetParameters"],
                                                     resources=["*"]
                                                 )
                                             ]
                                         )
                                     },
                                     managed_policies=[iam.ManagedPolicy.from_managed_policy_arn(self,'AmazonECSTaskExecutionRolePolicy',"arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"),
                                                       iam.ManagedPolicy.from_aws_managed_policy_name(
                                         "AWSXrayWriteOnlyAccess"),
                                         iam.ManagedPolicy.from_aws_managed_policy_name(
                                         "AWSXRayDaemonWriteAccess"),
                                         iam.ManagedPolicy.from_aws_managed_policy_name("AmazonPrometheusRemoteWriteAccess")])
        # 5. Otel Task Role
        otel_task_role = iam.Role(self, 'otel-task-role',
                                  path="/",
                                  assumed_by=iam.ServicePrincipal(
                                      "ecs-tasks.amazonaws.com"),
                                  inline_policies={
                                      'GetConfigParamters': iam.PolicyDocument(
                                          statements=[
                                              iam.PolicyStatement(
                                                  effect=iam.Effect.ALLOW,
                                                  actions=[
                                                      "logs:PutLogEvents",
                                                      "logs:CreateLogGroup",
                                                      "logs:CreateLogStream",
                                                      "logs:DescribeLogStreams",
                                                      "logs:DescribeLogGroups",
                                                      "xray:PutTraceSegments",
                                                      "xray:PutTelemetryRecords",
                                                      "xray:GetSamplingRules",
                                                      "xray:GetSamplingTargets",
                                                      "xray:GetSamplingStatisticSummaries",
                                                      "aps:RemoteWrite",
                                                      "ssm:GetParameters"],
                                                  resources=["*"]
                                              )
                                          ]
                                      )
                                  },
                                  managed_policies=[iam.ManagedPolicy.from_managed_policy_arn(self,'AmazonECSTaskExecutionRolePolicyTaskRole',"arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"),
                                                    iam.ManagedPolicy.from_aws_managed_policy_name(
                                      "AWSXrayWriteOnlyAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name(
                                      "AWSXRayDaemonWriteAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AmazonPrometheusRemoteWriteAccess")])
        ## 6. Otel Service Logs group builder
        otel_service_logs_group = logs.LogGroup(self,'otel-service-ecs-log-group',
                                   log_group_name="/otel/service/log",
                                   removal_policy=RemovalPolicy.DESTROY,
                                   retention=logs.RetentionDays.TWO_WEEKS
                                   )
        ## 6. Otel Service Task Defination
        otel_service_task_def = ecs.TaskDefinition(self,'otel-service-task-defination',
                                                   memory_mib="512",
                                                   cpu="256",
                                                   execution_role=otel_service_role,
                                                   task_role=otel_task_role,
                                                   compatibility=ecs.Compatibility.FARGATE,
                                                   network_mode=ecs.NetworkMode.AWS_VPC)
        otel_service_task_def.add_container(service_name,
                                            container_name="otel-service",
                                            image=ecs.ContainerImage.from_registry(
                                                "public.ecr.aws/aws-observability/aws-otel-collector:latest"
                                            ),
                                            essential=True,
                                            memory_limit_mib=512,
                                            logging=ecs.AwsLogDriver(log_group=otel_service_logs_group,
                                                                     stream_prefix="/ecs/"),
                                            port_mappings=[ecs.PortMapping(container_port = 4317),
                                                           ecs.PortMapping(container_port = 2000),
                                                           ecs.PortMapping(container_port = 8125)],
                                            secrets={"AOT_CONFIG_CONTENT":ecs.Secret.from_ssm_parameter(config_param)})

        ## 6. Otel Fargate Task
        ecs.FargateService(self,'OtelServiceFargate',
                                                 cluster=otel_cluster,
                                                 task_definition=otel_service_task_def,
                                                 service_name=service_name,
                                                 desired_count=1,
                                                 assign_public_ip=False,
                                                 cloud_map_options=ecs.CloudMapOptions(
                                                     cloud_map_namespace=privatednsnamespace,
                                                     dns_ttl=Duration.seconds(60),
                                                     name=service_name,
                                                     dns_record_type=servicediscovery.DnsRecordType.A),
                                                 security_groups=[otel_security_group],
                                                 vpc_subnets=ec2.SubnetSelection(
                                                  subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                                ))
