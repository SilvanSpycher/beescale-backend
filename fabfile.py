import datetime
import os
import re
import time
from contextlib import contextmanager
from typing import Optional

import requests
import toml
from fabric.api import cd, env, get, prefix, put, run, sudo, task
from fabric.contrib.files import exists

# Define the project's name.
# This string can only contain [a-z-_0-9]!
from application.env_utils import Env, load_yaml_env

###
# --- START CONFIGURATION HERE ---
###

PROJECT_NAME = 'beescale'

# The projects git url (prefer SSH over HTTPS).
REPO_URL = ''

# Set this to the INTERNAL slack channel.
SLACK_CHANNEL = '#api'

# Services that need to be restarted after deployment.
# By default, the following services are restarted:
# - uwsgi
# - nginx
# - (memcached) -> if python-memcached is a dependency
# - (redis) -> if django_redis is a dependency
ADDITIONAL_SERVICES = []

# Additional management tasks that need to be executed after deployment (without the './manage.py' part).
# Example: if you want to register the crontab for django-crontab, add 'crontab add' to the list.
ADDITIONAL_MANAGE_TASKS = []

# Configure your target hostnames per environment
HOSTS = {
    'test': 'test.beescale.ch',
    'production': 'beescale.ch'
}

###
# --- NO CHANGES BELOW THIS LINE ---
###

# assert configuration
assert PROJECT_NAME != '', 'PROJECT_NAME is not set, aborting.'
assert re.match('[a-z-_0-9]', PROJECT_NAME), 'PROJECT_NAME contains invalid characters, aborting'
assert REPO_URL != '', 'REPO_URL is not set, aborting.'
assert SLACK_CHANNEL != '', 'SLACK_CHANNEL is not set, aborting.'

# set up fabric environment
env.branch = 'master'
env.user = 'ubuntu'

# set defaults
UWSGI_HOME = f'/etc/uwsgi/sites'
USER_HOME = f'/home/{env.user}'
VENVS_ROOT = f'{USER_HOME}/venvs'
PROJECT_APP_NAME = 'application'
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# import Pipfile for determining python version and dependencies
parsed_pipfile = toml.load(os.path.join(BASE_DIR, 'Pipfile'))

assert parsed_pipfile is not None, 'Could not load Pipfile, aborting.'
python_version = parsed_pipfile['requires']['python_version']
assert python_version is not None, 'Could not determine python version using Pipfile, aborting.'

# register additional services to restart based on package dependencies
if 'python-memcached' in parsed_pipfile['packages'].keys() and 'memcached' not in ADDITIONAL_SERVICES:
    ADDITIONAL_SERVICES.append('memcached')

if 'django_redis' in parsed_pipfile['packages'].keys() and 'redis' not in ADDITIONAL_SERVICES:
    ADDITIONAL_SERVICES.append('redis')


@task
def test():
    assert HOSTS['test'] != '', 'Hostname for test environment is not set, aborting.'
    env.host = env.host_string = HOSTS['test']
    env.environment = 'test'
    env.branch = 'develop'


@task
def production():
    assert HOSTS['production'] != '', 'Hostname for production environment is not set, aborting.'
    env.host = env.host_string = HOSTS['production']
    env.environment = 'production'


@task
def deploy():
    _set_fabric_env()

    start_time = time.time()
    if not exists(env.repo_path):
        run(f'mkdir -p {env.repo_path}')

    with cd(env.repo_path):
        # git
        if exists('.git'):
            run('touch .maintenance_in_progress')
            run(f'git checkout {env.branch}')
            run(f'git pull -q origin {env.branch}')
        else:
            run(f'git clone -q {REPO_URL} -b {env.branch} .')
            run('touch .maintenance_in_progress')

        # application deployment
        with source_virtualenv():
            run('pip install -q --upgrade pip pipenv')
            run('pipenv sync')

            # build frontend assets
            run('yarn --silent')
            run('yarn run build')

            # migrate and collect static assets
            run('./manage.py migrate')
            run('./manage.py collectstatic --noinput')

            # run additional management tasks
            for manage_task in ADDITIONAL_MANAGE_TASKS:
                run(f'./manage.py {manage_task}')

            ensure_superuser()

        # fetch git infos for slack announcement
        git_info = run('git log --oneline -n 1 --no-merges --no-color | cat')

        run('rm .maintenance_in_progress')

    restart_services()

    check_for_gitlab_ci_key()

    end_time = time.time()
    time_taken = str(round(end_time - start_time, 2))
    announce_slack(time_taken, git_info)

    save_env()


def restart_services():
    uwsgi_file = os.path.join(UWSGI_HOME, f'{env.venv_name}.ini')

    # restart uWSGI and nginx by default
    run(f'touch {uwsgi_file}')
    sudo('/usr/sbin/service nginx reload', shell=False)

    # restart all additional services
    for service in ADDITIONAL_SERVICES:
        sudo(f'/usr/sbin/service {service} restart')


def _set_fabric_env():
    env.venv_name = f'{PROJECT_NAME}-{env.environment}'
    env.target_url = f'https://{env.host}'
    env.venv_root = os.path.join(VENVS_ROOT, env.venv_name)
    env.repo_path = os.path.join(env.venv_root, 'repository')


@contextmanager
def source_virtualenv():
    venv_root = os.path.join(VENVS_ROOT, env.venv_name)
    if not exists(os.path.join(venv_root, 'bin')):
        run(f'virtualenv -p python{python_version} {venv_root}')

    with prefix('source ' + os.path.join(venv_root, 'bin/activate')):
        with prefix(f'export DJANGO_SETTINGS_MODULE={PROJECT_APP_NAME}.settings'):
            yield


def ensure_superuser():
    get_env()
    with source_virtualenv():
        # make sure needed variables are defined
        REMOTE_ENV.get('SUPERUSER', {})
        REMOTE_ENV.SUPERUSER.get('USERNAME', 'admin')
        REMOTE_ENV.SUPERUSER.get_password('PASSWORD')
        save_env()
        # ensure a super user was created
        run(f'python {env.repo_path}/ensure-superuser.py')


def announce_slack(time_taken, git_info):
    slack_data = {
        'channel': SLACK_CHANNEL,
        'username': 'deploy-bot',
        'attachments': [{
            'pretext': 'Deployed successfully, took me {} seconds'.format(time_taken),
            'title': '{} ({})'.format(env.venv_name, env.target_url),
            'fields': [{
                'value': ':speech_balloon: {}'.format(git_info), 'short': 'false'
            }],
            'footer': '{:%d %B %Y}'.format(datetime.date.today()),
            'color': 'good'
        }],
        'icon_emoji': ':ok_hand:'
    }

    res = requests.post(SLACK_WEBHOOK_URL, json=slack_data)
    if res.status_code != 200:
        raise ValueError(
            'Request to slack returned an error {}, the response is:n{}'.format(res.status_code, res.text)
        )


REMOTE_ENV: Optional[Env] = None
ENV_PATH = '.env.yaml'


def get_env():
    global REMOTE_ENV

    filename = f'{env.host}.env.yaml'

    # get from remote, if exists ...
    print(os.path.join(env.repo_path, ENV_PATH))
    if exists(os.path.join(env.repo_path, ENV_PATH)):
        get(os.path.join(env.repo_path, ENV_PATH), filename)
    else:
        open(filename, 'a')

    REMOTE_ENV = load_yaml_env(filename)
    REMOTE_ENV.get('PROJECT_NAME', PROJECT_NAME)


def save_env():
    REMOTE_ENV.persist()
    if exists(env.repo_path):
        put(current_host_env_file(), os.path.join(env.repo_path, '.env.yaml'))


def current_host_env_file(local=False) -> str:
    filename = f'{env.host}.env.yaml'
    if local:
        return os.path.join(BASE_DIR, filename)
    return filename


@task
def check_for_gitlab_ci_key():
    if run(f"cat {USER_HOME}/.ssh/authorized_keys | grep 'wZT4RVjjzhtcQr/1qgKGt'", warn_only=True, quiet=True).failed:
        # is empty
        print('||| GitLab CI key not found in ~/.ssh/authorized_keys. Make sure to put it there. |||')
