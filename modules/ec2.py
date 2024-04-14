import pulumi
import pulumi_aws as aws

class EC2Instance:
    """
    A reusable module for creating an EC2 instance.
    """
    def __init__(self, name, ami, instance_type, key_name, vpc_security_group_ids, subnet_id, user_data=None, tags=None):
        self.instance = aws.ec2.Instance(name,
            ami=ami,
            instance_type=instance_type,
            key_name=key_name,
            vpc_security_group_ids=vpc_security_group_ids,
            subnet_id=subnet_id,
            user_data=user_data,
            tags=tags
        )

        pulumi.export('instance_id', self.instance.id)
        pulumi.export('public_ip', self.instance.public_ip)
        pulumi.export('private_ip', self.instance.private_ip)

# Example usage:
# import ec2_instance
# my_ec2_instance = ec2_instance.EC2Instance('my-ec2-instance', 'ami-12345', 't2.micro', 'my-key-pair',
#                                            ['sg-12345'], 'subnet-67890', user_data='#!/bin/bash\necho "Hello, World!"',
#                                            tags={'Name': 'my-server'})
