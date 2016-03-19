import os
import math
import shutil
import pytoml
import socket

import ctypes
import platform
import sys

app_name = 'fatbot'


# define filesystem paths

from xdg import BaseDirectory
package_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = BaseDirectory.save_config_path(app_name)
data_dir = BaseDirectory.save_data_path(app_name)
cache_dir = BaseDirectory.save_cache_path(app_name)
#runtime_dir = BaseDirectory.get_runtime_dir(app_name) # XDG_RUNTIME_DIR undefined in systemd?
runtime_dir = cache_dir

config_file = os.path.join(config_dir, 'config.toml')


# load config file

if not os.path.isfile(config_file):
    shutil.copyfile(os.path.join(package_dir, 'examples', 'config.toml'), config_file)

with open(config_file) as config_file_object:
    settings = pytoml.load(config_file_object)


# copy version number to settings
from version import __version__
settings['bot']['version'] = __version__


# where pid file is stored
settings['bot']['runtime_dir'] = runtime_dir



# define database connection

import sqlite3

def db_connect():
    db = sqlite3.connect( os.path.join(data_dir, app_name + '.db') )
    db.row_factory = sqlite3.Row

    # initialize tables if none exist
    table_count = db.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    if table_count is 0:
        settings['bot']['first_run'] = True
        f = open(os.path.join(package_dir, 'examples', 'db.sql'),'r')
        db.executescript(f.read())

    return db

