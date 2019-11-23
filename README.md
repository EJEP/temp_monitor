# Monitor temperature #

Monitor temperature from a sensor and display on a webpage.

Currently both the monitoring script and the webpage are in the same repository. This may change.

Inspired by https://github.com/Pyplate/rpi_temp_logger.

## Monitor Script ##

This script reads the temperature from a DS18B20 temperature sensor and two weather services (OpenWeatherMap and the Met Office) and stores all the information in a database.

### Requirements ###

#### Python #####

+ [pyowm](https://github.com/csparpa/pyowm)
+ [datapoint](https://github.com/jacobtomlinson/datapoint-python)
+ [w1thermsensor](https://github.com/timofurrer/w1thermsensor)
+ [pyserial](https://github.com/pyserial/pyserial)

API keys are required for the [OpenWeatherMap API](https://openweathermap.org/api) and the MetOffice [Datapoint API](https://www.metoffice.gov.uk/datapoint).

#### Non-python ####

+ SQLite

### Setup ###

The `flask init-db` command provided by the flask app initialises a database in the `instance` directory of the webpage installation. This is described below. See `schemal.sql` for the creation of the database. The web server will need to be able to read this file.

### Configuration ###

The configuration is done in `config.py`. This stores the API keys and the coordinates of the location for the weather.

The variables in `config.py` are:

+ `OWM_API_KEY`: The API key for OpenWeatherMap.
+ `DATAPOINT_API_KEY`: The API key for datapoint.
+ `COORDS`: The coordinates to use for the weather reporting, in decimal latitude/longitude.

### Hardware ###

See, for instance, this [tutorial](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing?view=all) from Adafruit for information on wiring up a DS18B20 sensor with a Raspberry Pi.


## Web Page ## 

The web page shows the temperature on a graph using [Bokeh](https://bokeh.pydata.org/en/latest/). [Flask](http://flask.pocoo.org/) is used to display the page.

Currently I have not written the code to integrate the code with servers other than apache, but flask is capable of integrating with others. See the flask deployment [docs](http://flask.pocoo.org/docs/1.0/deploying/) for more information.

### Requirements ###

If the project is installed, the dependencies are set in `setup.py`.

+ [Bokeh](https://bokeh.pydata.org/en/latest/)
+ [Flask](http://flask.pocoo.org/)
+ [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
+ [WTForms](https://wtforms.readthedocs.io/en/stable/)

### Configuration ###

The `secret_key` configuration variable for flask needs to be set in a `config.py` file in the flask instance directory.

### Installation ###

The package can be installed using pip, the flask docs describe how this can be done. When the package us installed, the instance directory is `$INSTALL_PREFIX/var/instance`. This is described in the flask [docs](http://flask.pocoo.org/docs/1.0/config/).

Once installed, the database can be created. The process is documented in the flask docs. To do this, run

```
export FLASK_APP=temp_monitor_web
flask init-db
```

This creates the database in an instance directory in the virtualenv the app is installed in.

The integration with a server is dependent on the server. Different operating systems may also put server configuration files in different places.


#### Apache with mod_wsgi ####

The python code is written in python 3. `mod_wsgi` cannot run across python versions, so ensure that the version of mod_wsgi which supports python 3 is installed. The `mod_wsgi` [documentation](https://modwsgi.readthedocs.io/en/develop/) contains instructions on how to install and set up `mod_wsgi`. As noted in the [docs](https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html) it is easier to use `mod_wsgi` with virtual environments if the environment is created using `virtualenv` rather than `venv`. This is because `virtualenv` includes an `activate_this.py` file. The flask [documentation](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/#working-with-virtual-environments) for using virtual environments with apache and `mod_wsgi` suggests how to use this in a `.wsgi` file. The `templog.wsgi` file is as follows:

```
python_home = '/path/to/venv'

activate_this = python_home + '/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

from webpage import create_app
application = create_app()
```

The `mod_wsgi` documentation describes how to set up a wsgi script with apache. The configuration I have used is below:
```
WSGIDaemonProcess templog threads=2 python-home=/path/to/empty/venv
WSGIScriptAlias /templog /path/to/wsgi_dir/templog.wsgi process-group=templog
WSGIProcessGroup templog

<Directory /path/to/wsgi_dir>
    <IfVersion < 2.4>
        Order allow,deny
        Allow from all
    </IfVersion>
    <IfVersion >= 2.4>
        Require all granted
    </IfVersion>
</Directory>
```

This configuration is in a `.conf` file, in a `VirtualHost` definition in apache installed on raspbian.

Note that for this code, `WSGIScriptAlias` seems to need to be `WSGIScriptAlias / /path/to/wsgi_dir/templog.wsgi`. This is not the case in the `mod_wsgi` example [here](https://modwsgi.readthedocs.io/en/develop/user-guides/quick-configuration-guide.html).
