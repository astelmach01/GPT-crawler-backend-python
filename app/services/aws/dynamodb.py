import logging
from typing import Mapping

import boto3
from mypy_boto3_dynamodb.type_defs import AttributeValueUpdateTypeDef

from app.settings import settings

REGION = "us-east-2"
SUCCESS = 200

client = boto3.client(
    "dynamodb",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=REGION,
)


def put_item(
    table_name: str, table_key: str, **kwargs: Mapping[str, AttributeValueUpdateTypeDef]
) -> bool:
    """
    Put an item into a table.

    :param table_name: name of the table.
    :param table_key: key of the item to put.
    :param kwargs: attributes to put.

    :return: True if the item was put, False otherwise.
    """
    item = {}

    for key, value in kwargs.items():
        item[key] = {"Value": {"S": str(value)}, "Action": "PUT"}

    logging.info(f"Putting item {item} with key {table_key}")
    response = client.update_item(
        TableName=table_name,
        Key={"user": {"S": table_key}},
        AttributeUpdates=item,  # type: ignore
    )
    return response["ResponseMetadata"]["HTTPStatusCode"] == SUCCESS


def get_attribute(table_name: str, key: str, attribute: str) -> str | None:
    """
    Get an attribute from a table.

    :param table_name: name of the table.
    :param key: key of the item to get.
    :param attribute: attribute to get.

    :return: attribute value if the item exists, None otherwise.
    """
    logging.info(f"Getting attribute '{attribute}' for key '{key}'")
    response = client.get_item(TableName=table_name, Key={"user": {"S": key}})
    item = response.get("Item")

    if not item or not (value := item.get(attribute)):
        return None

    return value["S"]


def delete_item(table_name: str, key: str) -> bool:
    """
    Delete an item from a table.

    :param table_name: name of the table.
    :param key: key of the item to delete.
    :return: True if the item was deleted, False otherwise.
    """
    logging.info(f"Deleting item {key}")
    response = client.delete_item(TableName=table_name, Key={"user": {"S": key}})
    return response["ResponseMetadata"]["HTTPStatusCode"] == SUCCESS
