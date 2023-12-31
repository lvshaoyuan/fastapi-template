#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append('../../')

from app.core.serve import db_config  # noqa
from app.models import models  # noqa

TORTOISE_ORM = {
    "connections": db_config['connections'],
    "apps": {
        "models": {
            "models": ["aerich.models", *models],
            "default_connection": "default",
        },
    },
}
