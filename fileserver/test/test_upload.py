# -*- coding: utf-8 -*-
"""
    fileserver.test.test_upload
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit testing uploading module

    :copyright: (c) 2016 by Saeed Abdullah.

"""

import os
import glob
import unittest2
from cStringIO import StringIO
import warnings

from fileserver import app


class UploadTestCase(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = app.test_client()
        cls.app.config["TESTING"] = True

    def test_upload(self):
        content = "Upload data"
        fname = "data.txt"
        name_key = self.app.config["UPLOADED_FILE_NAME_KEY"]
        r = self.client.post("/upload/",
                             data={name_key: (StringIO(content), fname)})

        self.assertEqual(r.status_code, 200)

        l = glob.glob(os.path.join(app.config["UPLOAD_FOLDER_PATH"],
                                   "{0}*".format(fname)))
        if len(l) > 1:
            warnings.warn("More than 1 file found: {0}".format(l))

        with open(l[0]) as f:
            s = f.read()
        self.assertEqual(s, content)
