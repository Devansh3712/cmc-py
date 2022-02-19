#!/usr/bin/env python

"""Module for saving API calls as cache using Redis."""

import json
import os
from typing import Any, Dict
import redis
from api.utils.config import settings


class Database:
    """Class for CRUD operations on the Redis cache server."""

    def __init__(self) -> None:
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.parent_dir = os.path.dirname(self.current_dir)
        self.host = "localhost" if settings.host is None else settings.host
        self.port = 6379 if settings.port is None else settings.port
        self.expire = 600 if settings.expire is None else settings.expire
        self.database = redis.Redis(self.host, self.port)

    def add_data(self, name: str, data: Dict[str, Any]) -> bool:
        """Add data to the redis cache server.

        Args:
            name (str): Name of the key.
            data (Dict[str, Any]): Data for the key.

        Returns:
            bool: True if data is added to cache else False.
        """
        try:
            self.database.setex(name, self.expire, json.dumps(data, default=str))  # type: ignore
            return True
        except:
            return False

    def check_data(self, name: str) -> bool:
        """Check if the given key exists in the redis cache server.

        Args:
            name (str): Name of the key.

        Returns:
            bool: True if key exists in cache else False.
        """
        result = self.database.get(name)
        if result:
            return True
        return False

    def get_data(self, name: str) -> Dict[str, Any] | bool:
        """Get data from the redis cache server.

        Args:
            name (str): Name of the key.

        Returns:
            Dict[str, Any] | bool: Data of key if it exists else False.
        """
        check = self.check_data(name)
        if check:
            data = self.database.get(name)
            result = json.loads(data.decode("utf-8"))  # type: ignore
            return result
        else:
            return False
