from aws_cdk import aws_ecs as ecs


def otel_cluster_create(self, vpc,service_name):
    return ecs.Cluster(self, service_name,
                                   cluster_name='otel',
                              vpc=vpc, container_insights=True)

