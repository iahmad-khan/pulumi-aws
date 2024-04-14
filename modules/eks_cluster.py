# eks_cluster.py

import pulumi_eks as eks
import pulumi_aws as aws

class EksCluster:
    def __init__(self, name, kubernetes_version, enable_fargate, instance_type='t2.medium', desired_capacity=2, min_size=1, max_size=3):
        self.kubernetes_version = kubernetes_version
        self.enable_fargate = enable_fargate

        self.cluster = eks.Cluster(
            name,
            version=self.kubernetes_version,
            instance_type=instance_type,
            desired_capacity=desired_capacity,
            min_size=min_size,
            max_size=max_size,
            create_oidc_provider=True,
            enabled_cluster_log_types=['api', 'audit', 'authenticator'],
            deploy_dashboard=False
        )

        if self.enable_fargate:
            # Define the Fargate profile here if Fargate is enabled.
            role = aws.iam.Role('fargatePodExecutionRole', assume_role_policy=json.dumps({
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'sts:AssumeRole',
                    'Principal': {
                        'Service': 'eks-fargate-pods.amazonaws.com'
                    },
                    'Effect': 'Allow',
                    'Sid': ''
                }]
            }))

            policy_attachment = aws.iam.RolePolicyAttachment('fargatePodExecutionRolePolicyAttachment',
                role=role.id,
                policy_arn='arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy'
            )

            self.fargate_profile = aws.eks.FargateProfile(
                'my-fargate-profile',
                cluster_name=self.cluster.eks_cluster.name,
                pod_execution_role_arn=role.arn,
                selectors=[{
                    'namespace': 'default'
                }],
                opts=pulumi.ResourceOptions(depends_on=[self.cluster, policy_attachment])
            )

        pulumi.export('kubeconfig', self.cluster.kubeconfig)
