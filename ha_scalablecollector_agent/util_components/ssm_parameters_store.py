import yaml
from aws_cdk import (
    aws_ssm as ssm,
)

def configure_ssm_parameters(self, parameter_name, config_yaml):
    return ssm.StringParameter(self, 'otel-aot-config-paramter',
                                               parameter_name=parameter_name,
                                               tier=ssm.ParameterTier.ADVANCED,
                                               data_type=ssm.ParameterDataType.TEXT,
                                               string_value=yaml.dump(config_yaml))
