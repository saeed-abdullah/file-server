# -*- coding: utf-8 -*-
"""
    fileserver.default_config
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Default configurations to be used in the application.

    :copyright: (c) 2016 by Saeed Abdullah.
"""

DEBUG = False

UPLOAD_FOLDER_PATH = "./"  # uploaded folder.
UPLOADED_FILE_NAME_KEY = "data"  # File name as in <input type=file> tag.
FILE_NAME_SUFFIX_FUNCTION = None  # Default is seconds since epoch

MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # Maximum size of file is 64 MB
