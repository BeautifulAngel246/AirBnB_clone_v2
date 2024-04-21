#!/usr/bin/python3
# Fabric Script that creates and distributes an archive to your web servers

from fabric.api import env


<<<<<<< HEAD
env.hosts = ["100.25.188.187", "34.204.60.71"]
=======
env.hosts = ["18.235.233.119", "54.157.186.128"]
>>>>>>> 49bd87c88737583586acce8fc87937c1124cef18
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    from fabric.api import local
    from datetime import datetime

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    local("tar -cvzf {} web_static".format(file))
    return file


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    from fabric.api import env, put, run
    import os

    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        folder = "/data/web_static/releases/"
        + archive_path.split("/")[-1][:-4]
        run("mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{}.tgz -C {}"
            .format(archive_path.split("/")[-1][:-4], folder))
        run("rm /tmp/{}.tgz".format(archive_path.split("/")[-1][:-4]))
        run("mv {}/web_static/* {}/".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
