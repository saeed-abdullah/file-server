# -*- coding: utf-8 -*-
"""
    fileserver
    ~~~~~~~~~~

    Simple fileserver based on Flask.

    :copyright: (c) 2016 by Saeed Abdullah.

"""
from __future__ import absolute_import

from flask import Flask, request
from werkzeug import secure_filename
import os
import time

# Creates the app
app = Flask(__name__)

# Loads default config
from . import default_config
app.config.from_object(default_config)
app.config.from_envvar("FILE_SERVER_SETTINGS")


@app.route("/upload/", methods=["POST"])
def upload_file():
    """ Saves uploaded file to the given directory. """

    folder = app.config["UPLOAD_FOLDER_PATH"]
    suffix_f = app.config["FILE_NAME_SUFFIX_FUNCTION"]

    if suffix_f is None:
        suffix_f = default_suffix_function

    f = request.files[app.config["UPLOADED_FILE_NAME_KEY"]]

    name = "{0}{1}".format(secure_filename(f.filename),  # secure filename
                           suffix_f(f))

    f.save(os.path.join(folder, name))

    return "", 200


def default_suffix_function(f):
    return "_{0}".format(time.time())
