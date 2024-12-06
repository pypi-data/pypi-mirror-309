"""MongoDB Connector"""

from contextlib import contextmanager
from time import sleep
from typing import Union

import six

from django.conf import settings

from mongoengine import connect
from mongoengine.base import BaseDocument
from mongoengine.errors import MongoEngineException

from swifty.logging.logger import SwiftyLoggerMixin


@contextmanager
def connect_to_db(db, alias, count=3):
    """
    _summary_

    Args:
        db (_type_): _description_
        alias (_type_): _description_
        count (int, optional): _description_. Defaults to 3.

    Raises:
        MongoEngineException: _description_
    """
    retry_count = 0
    exception = None
    while retry_count < count:
        try:
            connect(host=f"{settings.MONGO_URL}", db=db, alias=alias)
            yield
            # return
        except (MongoEngineException, ConnectionError) as ex:
            retry_count += 1
            exception = six.text_type(ex)
            sleep(0.3)  # Wait 300ms before retrying

    raise MongoEngineException(
        f"Unable to connect to database after {count} attempts, specific error: {exception}"
    )


def mongo_connection(func):
    """
    Decorator which automatically reconnects mongo connection
    when connection or timeout errors occur.

    .. note::
        This function expects the wrapped function to
        have ``reconnect()`` method.
    """

    def wrapper(self, *args, mongo_collection=None, **kwargs):
        """_summary_

        Raises:
            MongoEngineException: _description_
            MongoEngineException: _description_

        Returns:
            _type_: _description_
        """

        mongo_collection = (
            mongo_collection or self and getattr(self, "mongo_collection", None)
        )

        if not mongo_collection or not issubclass(mongo_collection, BaseDocument):
            raise MongoEngineException("Mongo collection is not defined")

        metadata = getattr(mongo_collection, "_meta", {})

        db = metadata and metadata.get("db_name", None)

        if not db:
            raise MongoEngineException("Mongo DB is not defined")

        alias = metadata and metadata.get("db_alias", "default")

        with connect_to_db(db=db, alias=alias):
            return func(self, *args, mongo_collection=None, **kwargs)

    return wrapper


class MongoConnector(SwiftyLoggerMixin):
    """_summary_

    Args:
        SwiftyLoggerMixin (_type_): _description_
    """

    def __init__(self, mongo_collection) -> None:
        if not mongo_collection or not issubclass(mongo_collection, BaseDocument):
            raise MongoEngineException("Mongo collection is not defined")

        self.mongo_collection = mongo_collection
        self.mongo_objects = getattr(mongo_collection, "objects")

    @mongo_connection
    def insert(self, data: dict):
        """_summary_

        Args:
            data (_type_): _description_
        """

        self.mongo_objects.insert(self.mongo_collection(**data))

    @mongo_connection
    def insert_many(self, list_of_data: list[dict]):
        """_summary_

        Args:
            list_of_data (_type_): _description_
        """

        self.mongo_objects.insert(
            [self.mongo_collection(**data) for data in list_of_data],
        )

    @mongo_connection
    def update(self, data, filters: Union[dict, None] = None, q_combine=None):
        """_summary_

        Args:
            data (_type_): _description_
            filters (_type_, optional): _description_. Defaults to None.
            qCombine (_type_, optional): _description_. Defaults to None.
        """

        self.mongo_objects(q_combine, **(filters or {})).update(__raw__={"$set": data})

    @mongo_connection
    def update_many(self, list_of_data: list[dict]):
        """_summary_

        Args:
            list_of_data (_type_): _description_
        """

        self.mongo_objects.replace(
            [self.mongo_collection(**data) for data in list_of_data],
        )
