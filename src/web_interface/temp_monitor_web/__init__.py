import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config.from_mapping(
        # I think it is safe to leave this uncommented as the SECRET_KEY value
        # should be updated by the config file.
        #SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'templog.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import templog
    app.register_blueprint(templog.bp)

    return app
