python_home = '/path/to/venv'

activate_this = python_home + '/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

from webpage import create_app

application = create_app()
