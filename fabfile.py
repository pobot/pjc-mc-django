# -*- coding: utf-8 -*-

from fabric.api import task, env
from fabric.contrib.project import rsync_project

__author__ = 'Eric Pascual'

env.hosts = ['eric-laptop.local']
env.use_ssh_config = True


@task
def deploy():
    rsync_project(
        remote_dir='pjc-mc/',
        local_dir='./',
        exclude=[
            '.*',
            'fabfile.py',
            '*.pyc',
            '__pycache__',
            'db.sqlite3',
            'data',
            'requirements-dev.txt',
            'staticfiles',
            'teams.txt',
            'tests',
            'pytest.ini',
        ],
        default_opts='-arh'
    )
