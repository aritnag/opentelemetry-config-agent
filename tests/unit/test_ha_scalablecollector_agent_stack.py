import aws_cdk as core
import aws_cdk.assertions as assertions

from ha_scalablecollector_agent.ha_scalablecollector_agent_stack import HaScalablecollectorAgentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ha_scalablecollector_agent/ha_scalablecollector_agent_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HaScalablecollectorAgentStack(app, "ha_scalable-collector-agent")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
