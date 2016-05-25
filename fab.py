# -*- coding: utf-8 -*-
"""
    fab.py
    ~~~~~~~~

    Fabric script (largely copied from flask site).

"""
from fabric import api
import os

api.env.use_ssh_config = True
api.env.user = "saeed"


def pack():
    # create a new source distribution as tarball
    api.local("python setup.py sdist --formats=gztar", capture=False)


def deploy(destination_venv, wsgi_path=None):
    """
    Deploys the app.

    Parameters
    ----------

    destination_venv : str
        Destination virtualenv.

    wsgi_path : str
        WSGI file path. If not None, it would touch
        the file so that the app gets reloaded.


    Note
    ----
        For using fab from command line, you will need to pass
        the params in the following way:

        fab -f fab.py deploy:destination_venv="path_to_venv",wsgi_path="path_to_wsgi"
    """
    # figure out the release name and version
    dist = api.local("python setup.py --fullname", capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    api.put("dist/%s.tar.gz" % dist, "/tmp/fileserver.tar.gz")
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    api.run("mkdir /tmp/fileserver")
    with api.cd("/tmp/fileserver"):
        api.run("tar xzf /tmp/fileserver.tar.gz")

        with api.cd("{0}".format(dist)):
            # now setup the package with our virtual environment"s
            # python interpreter
            venv_python = os.path.join(destination_venv, "bin/python")
            api.sudo("{0} setup.py install".format(venv_python))
    # now that all is set up, delete the folder again
    api.sudo("rm -rf /tmp/fileserver /tmp/fileserver.tar.gz")

    if wsgi_path:
        # and finally touch the .wsgi file so that mod_wsgi triggers
        # a reload of the application
        api.sudo("touch {0}".format(wsgi_path))
