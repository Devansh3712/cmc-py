#!/usr/bin/env python

"""Module for formatting data returned by cmc-py modules."""

import json
from typing import Any


def format_data(data: Any, indent: int = 4) -> str:
    """Format the data dictionary returned by any class of
    the cmc-py modules.

    Args:
        data (Any): Data to be formatted.
        indent (int, optional): Indentation of the data. Defaults to 4.

    Returns:
        str: Formatted data.
    """
    if type(data) != dict:
        data = data.dict()
    result = json.dumps(data, indent=indent, default=str)
    return result
