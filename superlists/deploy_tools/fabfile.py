# -*- coding: utf-8 -*-
from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import settings
from fabric.api import sudo
from fabric.contrib.files import append
from fabric.contrib.files import exists
from fabric.contrib.files import sed

import random

REPO_URL = 'https://github.com/xuyan0/superlists.git'
SITE_NAME = 'superlists-staging.ashmemo.com'

# Using the Project Layout recommended by Two Scoops of Django
PROJECT_NAME = 'superlists'
CONFIG_APP_NAME = 'superlists'
PROJECT_DIR = '/' + PROJECT_NAME
CONFIG_APP_DIR = '/' + CONFIG_APP_NAME

# I still haven't discover any pratical solution to enable executing
# sudo commands using SSH Key authentication (without manually entering
# password for the sudo group user).
#
# env.key_filename = '~/.ssh/id_rsa'


def deploy():
    site_dir = '/home/{0}/sites/{1}'.format(env.user, env.host)
    site_src = site_dir + PROJECT_DIR
    site_subdirs = ('database', 'static', 'venv', PROJECT_NAME)
    repo_dir = '/home/{0}/sites/repos/{1}'.format(env.user, env.host)
    project_src = repo_dir + PROJECT_DIR


    _create_site_dir_struct(site_dir, site_subdirs)
    _create_repo_dir_struct(repo_dir)

    _update_repo(REPO_URL, repo_dir)
    _extract_project_to_site_dir(project_src, site_dir)

    _update_settings(site_src, CONFIG_APP_DIR, env.host)
    _update_virtualenv(site_src)
    _update_static_files(site_src)
    _update_database(site_src)

    _configure_nginx(site_src, SITE_NAME)
    _configure_gunicorn_systemd(site_src, SITE_NAME, PROJECT_NAME, CONFIG_APP_NAME)
    _restart_web_services()


def _create_site_dir_struct(dir, subdirs):
    for subdir in subdirs:
        run('mkdir -p {0}/{1}'.format(dir, subdir))


def _create_repo_dir_struct(dir):
    run('mkdir -p {0}'.format(dir))


def _update_repo(remote_url, repo_dir):
    if exists(repo_dir + '/.git'):
        with cd('{0}'.format(repo_dir)):
            run('git fetch')
    else:
        run('git clone {0} {1}'.format(remote_url, repo_dir))
    current_commit = local('git log -n 1 --format=%H', capture=True)
    with cd('{0}'.format(repo_dir)):
        run('git reset --hard {}'.format(current_commit))


def _extract_project_to_site_dir(project_src, site_dir):
    run('rm -rf {0}'.format(site_dir + PROJECT_DIR))
    run('cp -r {0} {1}'.format(project_src, site_dir))


def _update_settings(src_dir, config_app_dir, site_name):
    settings_file = src_dir + config_app_dir + '/settings.py'
    sed(settings_file, "DEBUG = True", "DEBUG = False")
    sed(settings_file,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["{%s}"]' % (site_name,)
    )
    secret_key_file = src_dir + config_app_dir + '/secret_key.py'
    if not exists(secret_key_file):
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[{]}'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(80))
        append(secret_key_file, "SECRET_KEY = '{0}'".format(key))
    append(settings_file, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(src_dir):
    virtualenv_dir = src_dir + '/../venv'
    if not exists(virtualenv_dir + '/bin/pip'):
        run('virtualenv --python=python3 {0}'.format(virtualenv_dir))
    run('{0}/bin/pip install -r {1}/requirements.txt'.format(virtualenv_dir, src_dir))


def _update_static_files(src_dir):
    with cd('{0}'.format(src_dir)):
        run('../venv/bin/python3 manage.py collectstatic --noinput'.format(src_dir))


def _update_database(src_dir):
    with cd('{0}'.format(src_dir)):
        run('../venv/bin/python3 manage.py migrate --noinput')


def _configure_nginx(src_dir, site_name):
    with cd('{0}'.format(src_dir)):
        # run('sed "s/SITENAME/%s/g" deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/%s' % (site_name, site_name,))
        with settings(line='$(sed "s/SITENAME/%s/g" deploy_tools/nginx.template.conf)' % (site_name,)):
            sudo('echo $line >> /etc/nginx/sites-available/{0}'.format(site_name))
    sudo('ln -sf /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s' % (site_name, site_name,))


def _configure_gunicorn_systemd(src_dir, site_name, project_name, config_app_name):
    with cd('{0}'.format(src_dir)):
        # run('sed "s/SITENAME/%s/g; s/PROJECT_NAME/%s/g; s/CONFIG_APP_NAME/%s/g" deploy_tools/gunicorn-systemd.template.conf | sudo tee /etc/systemd/system/gunicorn.service' % (site_name, project_name, config_app_name,))
        with settings(line='$(sed "s/SITENAME/%s/g; s/PROJECT_NAME/%s/g; s/CONFIG_APP_NAME/%s/g" deploy_tools/gunicorn-systemd.template.conf)' % (site_name, project_name, config_app_name,)):
            sudo('echo $line >> /etc/systemd/system/gunicorn.service')


def _restart_web_services():
    sudo('systemctl daemon-reload')
    sudo('systemctl start gunicorn')
    sudo('systemctl enable gunicorn')
    sudo('systemctl restart nginx')
