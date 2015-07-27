from fabric.api import env, run, cd

USERNAME = 'root'
SERVER = 'myfontsapi.marcfoley.co'
APP_NAME = 'myfontsapi'
PROJECT_DIR = '/var/www/myfontsapi'
WSGI_SCRIPT = 'application.wsgi'

env.hosts = ["%s@%	s" % (USERNAME, SERVER)]

def deploy():
    with cd(PROJECT_DIR):
        run('git pull')
        run('source flask/bin/activate')
        run('pip install -r requirements.txt')
        run('touch %s' % WSGI_SCRIPT)