import pulumi
import pulumi_aws as aws

class RedisModule:
    def __init__(self, name, subnet_group_name, engine_version="3.2.10", instance_class="cache.t2.micro"):
        # Create an ElastiCache Subnet Group
        self.subnet_group = aws.elasticache.SubnetGroup(
            f"{name}-subnet-group",
            subnet_ids=subnet_group_name
        )
        
        # Create an ElastiCache Security Group
        self.security_group = aws.ec2.SecurityGroup(
            f"{name}-security-group",
            description="Redis security group",
            ingress=[{
                'protocol': 'tcp',
                'from_port': 6379,
                'to_port': 6379,
                'cidr_blocks': ['0.0.0.0/0']
            }],
            egress=[{
                'protocol': '-1',
                'from_port': 0,
                'to_port': 0,
                'cidr_blocks': ['0.0.0.0/0']
            }]
        )

        # Create an ElastiCache Parameter Group
        self.parameter_group = aws.elasticache.ParameterGroup(
            f"{name}-parameter-group",
            family="redis3.2",
            description="Parameter group for Redis",
            parameters=[{
                'name': 'maxmemory-policy',
                'value': 'allkeys-lru'
            }]
        )

        # Create an ElastiCache Redis instance
        self.replication_group = aws.elasticache.ReplicationGroup(
            f"{name}-replication-group",
            replication_group_id=name,
            replication_group_description="Redis replication group",
            engine="redis",
            engine_version=engine_version,
            parameter_group_name=self.parameter_group.name,
            subnet_group_name=self.subnet_group.name,
            security_group_ids=[self.security_group.id],
            node_type=instance_class,
            number_cache_clusters=1,
            at_rest_encryption_enabled=True,
            transit_encryption_enabled=True,
            apply_immediately=True
        )

    # A method to retrieve the Redis cluster's primary endpoint.
    def get_primary_endpoint(self):
        return self.replication_group.primary_endpoint_address
