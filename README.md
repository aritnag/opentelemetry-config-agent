#### Nordcloud Engineering Blog : Enterprise implementation of Infra-as-Code using CDK
Refer to the [blog](https://medium.com/nordcloud-engineering/a-song-of-decentralization-and-observability-dance-with-open-telemetry-ec2c4d7006cf) for more details about the full implementation

This is an open source version of the OTEL Collector Agent written in Python language.
Solution Design of the Otel Collector Agent: ![Alt text](solution_design/Solution_Design.png?raw=true "Solution-Design")

Once tha above stack is deployed in the environment.
All the others ECS services can consume the endpoint via environment variables:
1. OTEL_EXPORTER_OTLP_ENDPOINT
2. OTEL_RESOURCE_ATTRIBUTES

#### Pre requisites:
Config Agent deployed stacks needs to be resolvable via AWS CloudMap and also the endpoints needs to be resolvable inside the ECS services.
  

### Deployment Framework

Change the account number and put in the relevant details to deploy the framework.
For End to end implementation using CD-CI, Please check [CDK end to end ](https://medium.com/nordcloud-engineering/enterprise-implementation-of-infra-as-code-using-cdk-5d229e08b414)

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `cdk deploy`      deploy this stack to your default AWS account/region


### Cleanup

 `cdk destroy`      Cleans up the stack


