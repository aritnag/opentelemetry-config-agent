import yaml
from aws_cdk import aws_ec2 as ec2  # Duration,


def retrieve_vpc(self, vpc_id):
     # Retrieve VPC information
    return ec2.Vpc.from_lookup(self, "VPC",
                                  vpc_id=vpc_id
                                  )
