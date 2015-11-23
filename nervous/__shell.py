#!/usr/bin/python -i
from database import setup_db

setup_db.setup_env()

from database import backend
from database import utils
from database import daemon
from database.models import *

if __name__ == '__main__':
    pass
