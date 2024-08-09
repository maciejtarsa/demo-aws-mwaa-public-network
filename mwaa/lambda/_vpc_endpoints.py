"""
This module provides functions for interacting with VPC Endpoints
"""

import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def tag_vpc_endpoint(service_name, tags):
    "A function to tag VPC endpoint"
    ec2_client = boto3.client("ec2")
    ec2_response = ec2_client.describe_vpc_endpoints(
        Filters=[{"Name": "service-name", "Values": [service_name]}]
    )
    for vpc_endpoint in ec2_response["VpcEndpoints"]:
        vpc_endpoint_id = vpc_endpoint["VpcEndpointId"]
        ec2_client.create_tags(
            Resources=[vpc_endpoint_id],
            Tags=[{"Key": k, "Value": v} for k, v in tags.items()]
        )
        logger.info("Vpc endpoint %s tagged successfully", vpc_endpoint_id)
