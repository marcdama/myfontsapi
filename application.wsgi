import os, sys

PROJECT_DIR = '/www/myfontsapi'

activate_this = os.path.join(PROJECT_DIR, 'flask', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from myfontsapi import app as application
