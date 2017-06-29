A simple file server on top of Flask.
(Flask-Uploads is a bit too complex for the use cases that I have).


The app will read config options from the file pointed by the environment variable: FILE_SERVER_SETTINGS.
So, you should set it before running the app (e.g., export FILE_SERVER_SETTINGS=config_file_path).


There are a number of config options that you should provide (see default_config.py for more details):

* UPLOAD_FOLDER_PATH: The directory location to save the uploaded file.

* UPLOADED_FILE_NAME_KEY: The name attribute in <input type=file> tag.

* FILE_NAME_SUFFIX_FUNCTION: Function to generate suffix for the saved filename. This is handy
    when there is a possibility of name collision (e.g., two files with same name from
    different users). Default is current second from unix epoch (so, as long as files
    with same name are not being uploaded at exactly same time, they would not be
    overloaded).

Installaion
===========

To install with Apache server and WSGI, you need to take the following steps:

1. Enable the site in the apache. This usually means adding the following lines in
the conf file (e.g., `/etc/apache2/sites-enabled/your_conf_file.conf`):

```

    ###### file-server #####
    WSGIDaemonProcess fileserver user=www-data group=www-data threads=5
    WSGIScriptAlias /fileserver /var/www/fileserver/fileserver.wsgi

    <Directory /var/www/fileserver>
        WSGIProcessGroup fileserver
        WSGIApplicationGroup %{GLOBAL}
        WSGIScriptReloading On
        Order deny,allow
        Allow from all
    </Directory>
```

If you want to have a different URL or folder, you should change
the WSGIScriptAlias and Directory params accrodingly.

2. Second, you'll need to create a virtualenv in the site folder: `virtualenv virtualenv`.

3. Create a folder for python eggs. `mkdir .python-egg`

4. Create the wsgi file (fileserver.wsgi) with following content:

```

activate_this='/var/www/fileserver/virtualenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Set up configurations
import os
os.environ['FILE_SERVER_SETTINGS'] = '/var/www/deploy_config/fileserver_deploy_config.py'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/fileserver/.python-egg'

import sys
sys.stdout=sys.stderr

from fileserver import app as application
```

5. Create the config file (/var/www/deploy_config/fileserver_deploy_config.py). You can
also update UPLOAD_FOLDER_PATH, FILE_NAME_SUFFIX_FUNCTION and UPLOADED_FILE_NAME_KEY
settings in the config file:

```
UPLOAD_FOLDER_PATH = '/var/www/path_to_upload_files/'
```
