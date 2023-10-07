#!/usr/bin/python3
""" Fabric script that generates a .tgz archive  and distributes it
to server """
from fabric.api import put, run, sudo, env
from datetime import datetime
import os

env.hosts = ["107.23.100.114", "35.153.17.86"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """ distributes an archive to your web servers """

    if not os.path.exsist(archive_path):
        return (False)

    check = put(archive_path, "/tmp/")
    if check.failed is True:
        return (False)
    file1 = archive_path.split("/")[-1].split(".")[0]
    path = "/data/web_static/releases/{}".format(file1)
    check = sudo(f"mkdir -p {path}")
    if check.failed is True:
        return (False)
    check = sudo(f"tar -xzf /tmp/{file1}.tgz -C {path}")
    if check.failed is True:
        return (False)
    check = sudo(f"rm -rf /tmp/{file1}.tgz")
    if check.failed is True:
        return (False)
    check = sudo(f"mv {path}/web_static/* {path}")
    if check.failed is True:
        return (False)
    check = sudo(f"ln -sf {path} /data/web_static/current")
    if check.failed is True:
        return (False)
    return (True)
