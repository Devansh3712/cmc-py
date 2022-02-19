#!/usr/bin/env python

"""Module for validating `config.yml` file."""

import os
from typing import Any, Dict, Optional
import yaml
from pydantic import BaseSettings


class Settings(BaseSettings):
    host: Optional[str]
    port: Optional[int]
    expire: Optional[int]


def load_yml() -> Dict[str, Any]:
    """Load Redis configurations from `config.yml` file.

    Returns:
        Dict[str, Any]: Redis configuration data.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(current_dir)
    root_dir = os.path.dirname(parent_dir)
    with open(os.path.join(root_dir, "config.yml")) as stream:
        data = yaml.safe_load(stream)
    return data["redis"]


yml_data = load_yml()
settings = Settings(**yml_data)
