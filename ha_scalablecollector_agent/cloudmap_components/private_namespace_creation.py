
import yaml
from aws_cdk import (
   
    aws_servicediscovery as servicediscovery,
    
    
)

def private_namespace_create(self,vpc,name):
    return servicediscovery.PrivateDnsNamespace(self, 'otel-privatednsnamespace',
                                                                   vpc=vpc,
                                                                   description="Private DNS Namespace for the services to resolve internally via the logical namespace",
                                                                   name=name)

