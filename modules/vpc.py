import pulumi_awsx as awsx

class VpcModule:
    def __init__(self, name, cidr_block="10.0.0.0/16"):
        self.vpc = awsx.ec2.Vpc(name,
            cidr_block=cidr_block,
            subnet_specs=[
                awsx.ec2.SubnetSpecArgs(
                    type="public",
                    cidr_mask=24,
                    name="public",
                ),
                awsx.ec2.SubnetSpecArgs(
                    type="private",
                    cidr_mask=24,
                    name="private",
                ),
            ],
            nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(
                strategy=awsx.ec2.NatGatewayStrategy.SINGLE
            ),
        )
        
        self.public_subnets = self.vpc.public_subnet_ids
        self.private_subnets = self.vpc.private_subnet_ids
        self.internet_gateway = self.vpc.internet_gateway
