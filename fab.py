# -*- coding: utf-8 -*-
"""
    fab.py
    ~~~~~~~~

    Fabric script (largely copied from flask site).

"""
from fabric import api

api.env.use_ssh_config = True
api.env.user = "saeed"


def pack():
    # create a new source distribution as tarball
    api.local("python setup.py sdist --formats=gztar", capture=False)


def deploy():
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
            api.sudo(("/var/www/fileserver/virtualenv/bin/python "
                      "setup.py install"))
    # now that all is set up, delete the folder again
    api.sudo("rm -rf /tmp/fileserver /tmp/fileserver.tar.gz")
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    api.sudo("touch /var/www/fileserver/fileserver.wsgi")
