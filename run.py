import sys, traceback
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

sys.path.append(BASEDIR)

from modules.background.sync import sync_all_tables

print(sync_all_tables())