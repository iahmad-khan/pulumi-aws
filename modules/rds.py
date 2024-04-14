import pulumi
import pulumi_aws as aws

class RdsModule:
    def __init__(self, name, db_engine, db_instance_class, username, password, allocated_storage, vpc_security_group_ids):
        # Initialize and create the RDS instance.
        self.db_instance = aws.rds.Instance(
            f"{name}-instance",
            engine=db_engine,
            instance_class=db_instance_class,
            allocated_storage=allocated_storage,
            db_subnet_group_name=name,
            db_name=name,
            username=username,
            password=password,
            skip_final_snapshot=True,
            vpc_security_group_ids=vpc_security_group_ids,
        )

    # A method to retrieve the RDS instance's endpoint.
    def get_endpoint(self):
        return self.db_instance.endpoint
