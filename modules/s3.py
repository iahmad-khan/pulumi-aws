import pulumi
import pulumi_aws as aws

class S3BucketManager:
    """
    Reusable module for creating and managing AWS S3 buckets.
    """
    def __init__(self, name, access_control=None, versioning=None, tags=None):
        """
        :param name: The name of the bucket.
        :param access_control: The canned ACL to apply (e.g., 'private', 'public-read').
        :param versioning: A boolean to enable/disable versioning.
        :param tags: A dictionary of tags to apply to the bucket.
        """
        self.bucket = aws.s3.Bucket(resource_name=name,
                                    acl=access_control,
                                    versioning=aws.s3.BucketVersioningArgs(
                                        enabled=True if versioning else False
                                    ),
                                    tags=tags)

        # Expose the bucket name and ARN as output properties of this module
        self.bucket_name = self.bucket.id
        self.bucket_arn = self.bucket.arn

# Example usage:
# Creating a private bucket with versioning enabled and custom tags
# private_bucket = S3BucketManager('my-private-bucket',
#                                 access_control='private',
#                                 versioning=True,
#                                 tags={'Environment': 'Dev', 'Project': 'DataStorage'})

# Creating a public-read bucket without versioning
# public_bucket = S3BucketManager('my-public-bucket',
#                                access_control='public-read',
#                                versioning=False)

# Export the bucket names and ARNs
# pulumi.export('private_bucket_name', private_bucket.bucket_name)
# pulumi.export('public_bucket_name', public_bucket.bucket_name)
# pulumi.export('private_bucket_arn', private_bucket.bucket_arn)
# pulumi.export('public_bucket_arn', public_bucket.bucket_arn)
