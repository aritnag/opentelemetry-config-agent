#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ha_scalablecollector_agent.ha_scalablecollector_agent_stack import HaScalablecollectorAgentStack


app = cdk.App()
HaScalablecollectorAgentStack(app, "HaScalablecollectorAgentStack",
    env=cdk.Environment(account='123456789', region='eu-west-1'),
    )

app.synth()
