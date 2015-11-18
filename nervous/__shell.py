#!/usr/bin/python -i
from database import setup_db

setup_db.setup_env()

from database import backend
from database import utils
from database import daemon

if (__name__ == '__main__'):
    setup_db.setup()
