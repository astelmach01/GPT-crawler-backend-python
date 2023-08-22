import logging
from typing import Any

import boto3

from app.settings import settings

REGION = "us-west-2"
SUCCESS = 200

client = boto3.client(
    "dynamodb",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="us-east-2",
)

USER_ACCESS_KEYS = "user-access-keys"
CHANNEL_ID_TO_PHONE_NUMBER = "channel_id-to-phone_number"


def make_key(table_name: str, key: str) -> dict[str, dict[str, str]]:
    """
    Return a formatted key for a given table name and key.

    :param table_name: name of the table.
    :param key: key of the item.

    :return: formatted key.
    """
    if table_name == USER_ACCESS_KEYS:
        return {"phone-number": {"S": key}}

    elif table_name == CHANNEL_ID_TO_PHONE_NUMBER:
        return {"channel_id": {"S": key}}

    return {"id": {"S": key}}


def put_item(table_name: str, table_key: str, **kwargs: dict[str, Any]) -> bool:
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
        Key=make_key(table_name, table_key),
        AttributeUpdates=item,
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
    response = client.get_item(TableName=table_name, Key=make_key(table_name, key))
    item = response.get("Item")

    return item.get(attribute)["S"] if item else None


def delete_item(table_name: str, key: str) -> bool:
    """
    Delete an item from a table.

    :param table_name: name of the table.
    :param key: key of the item to delete.
    :return: True if the item was deleted, False otherwise.
    """
    logging.info(f"Deleting item {key}")
    response = client.delete_item(TableName=table_name, Key=make_key(table_name, key))
    return response["ResponseMetadata"]["HTTPStatusCode"] == SUCCESS
