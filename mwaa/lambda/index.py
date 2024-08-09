"""
Lambda handler body
"""

import logging
from uuid import uuid4

import _cfnresponse
from _log_groups import tag_log_group
from _vpc_endpoints import tag_vpc_endpoint

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    "Lambda handler function"
    try:
        request_type = event["RequestType"]
        logger.info("request type is: %s", request_type)
        # pass resource id to all responses to prevent deletion when updating
        resource_id = event.get("PhysicalResourceId", str(uuid4()))
        input_data = event.get("ResourceProperties", {})
        log_group_arns = input_data.get("LogGroupArns")
        vpc_service_database = input_data.get("VPCDatabaseEndpointService")
        tags = input_data.get("Tags")

        if request_type in ["Create", "Update"]:
            if log_group_arns:
                for log_group_arn in log_group_arns:
                    logger.info("Tagging log group: %s", log_group_arn)
                    tag_log_group(log_group_arn, tags)
                
            if vpc_service_database:
                logger.info("Tagging vpc endpoint for: %s", vpc_service_database)
                tag_vpc_endpoint(vpc_service_database, tags)

            _cfnresponse.send(event, context, _cfnresponse.SUCCESS, {}, resource_id)

        if request_type == "Delete":
            # do nothing
            _cfnresponse.send(event, context, _cfnresponse.SUCCESS, {}, resource_id)
    except Exception as e:
        logger.error(e)
        _cfnresponse.send(event, context, _cfnresponse.FAILED, {"Message": str(e)}, resource_id)
