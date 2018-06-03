# -*- coding: utf-8 -*-

import os

from fabric.api import task, env, put
from fabric.contrib.project import rsync_project

__author__ = 'Eric Pascual'

env.hosts = ['eric-laptop.local']
env.use_ssh_config = True

remote_dir = 'pjc-mc/'


@task
def deploy(dry=False):
    rsync_project(
        remote_dir=remote_dir,
        local_dir='./',
        exclude=[
            '.*',
            'fabfile.py',
            '*.pyc',
            '__pycache__',
            '*.sqlite3',
            'data',
            'requirements-dev.txt',
            'staticfiles',
            'teams.txt',
            'tests',
            'pytest.ini',
        ],
        default_opts='-arh'
        extra_opts='--dry-run' if dry else ''
    )


@task
def deploy_db():
    put('./db.sqlite3', os.path.join(remote_dir, 'db.sqlite3'))
