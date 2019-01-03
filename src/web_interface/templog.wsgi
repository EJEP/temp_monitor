python_home = '/home/harri/temp_monitor/src/web_interface/venv2'

import sys
import site

# Calculate path to site-packages directory.

python_version = '.'.join(map(str, sys.version_info[:2]))
site_packages = python_home + '/lib/python%s/site-packages' % python_version
site.addsitedir(site_packages)

# Remember original sys.path.

prev_sys_path = list(sys.path)

# Add the site-packages directory.

site.addsitedir(site_packages)

