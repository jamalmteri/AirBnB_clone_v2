#!/usr/bin/python3
"""web server distribution"""
from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ["104.196.155.240", "34.74.146.120"]
env.key_filename = "~/id_rsa"

def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False
    try:
        archive_basename = os.path.basename(archive_path)
        archive_filename, _ = os.path.splitext(archive_basename)
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}'.format(archive_filename))
        main = "/data/web_static/releases/{}".format(archive_filename)
        run('tar -xzf /tmp/{} -C {}/'.format(archive_basename, main))
        run('rm /tmp/{}'.format(archive_basename))
        run('mv {}/web_static/* {}/'.format(main, main))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ "/data/web_static/current"'.format(main))
        return True
    except Exception as e:
        print(e)
        return False

