import pulumi
from modules.eks_cluster import EksCluster

# Parameters for the EKS cluster
cluster_name = 'my-eks-cluster'
kubernetes_version = '1.21'
enable_fargate = False

# Create the EKS cluster using the module
my_cluster = EksCluster(
    name=cluster_name,
    kubernetes_version=kubernetes_version,
    enable_fargate=enable_fargate
)

# Export the cluster's kubeconfig
pulumi.export('kubeconfig', my_cluster.cluster.kubeconfig)
