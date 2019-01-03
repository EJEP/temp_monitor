# Monitor temperature #

Monitor temperature from a sensor and display on a webpage.

Currently both the monitoring script and the webpage are in the same repository. This may change.

Inspired by https://github.com/Pyplate/rpi_temp_logger.

## Monitor Script ##

This script reads the temperature from a DS18B20 temperature sensor and two weather services (OpenWeatherMap and the Met Office) and stores all the information in a database.

### Requirements ###

+ SQLite
+ [pyowm](https://github.com/csparpa/pyowm)
+ [metoffer](https://github.com/sludgedesk/metoffer)
+ [w1thermsensor](https://github.com/timofurrer/w1thermsensor)

API keys are required for the [OpenWeatherMap API](https://openweathermap.org/api) and the MetOffice [Datapoint API](https://www.metoffice.gov.uk/datapoint).

### Setup ###

The `init-db` command in flask initialises a database in the `instance` directory of the webpage installation. See `schemal.sql` for the creation of the database.

### Configuration ###

The configuration is done in `config.py`. This stores the API keys and the coordinates of the location for the weather.

The variables in `config.py` are:

+ `OWM_API_KEY`: The API key for OpenWeatherMap.
+ `DATAPOINT_API_KEY`: The API key for datapoint.
+ `COORDS`: The coordinates to use for the weather reporting, in decimal latitude/longitude.


## Web Page ## 

The web page shows the temperature on a graph using [Bokeh](https://bokeh.pydata.org/en/latest/). [Flask](http://flask.pocoo.org/) is used to display the page.

Currently I have not written the code to integrate the code with a different server.

### Requirements ###

+ [Bokeh](https://bokeh.pydata.org/en/latest/)
+ [Flask](http://flask.pocoo.org/)
+ [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
+ [WTForms](https://wtforms.readthedocs.io/en/stable/)

### Configuration ###

The `secret_key` configuration variable for flask needs to be set in a `config.py` file in the flask instance directory.

### Installation ###

The package is distributed as a package installable with pip. The integration with a server is dependent on the server.

This was a pain. I will re-write this later.

+ Using `mod_wsgi` with virtual environments is a lot easier if the environment is created using `virtualenvironment` rather than `venv`.
+ As described [here](http://flask.pocoo.org/docs/1.0/config/) the instance directory is in `$PREFIX/var/`
+ `WSGIScriptAlias` needs to be `WSGIScriptAlias / /whatever/`. The first `/` is required.
+ Remember to read the Flask [docs](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/) on using virtual environments with a `.wsgi` file.
+ The example `.wsgi` file `from yourapplication import app as application` doesn't seem to work if there is a factory function in an `__init__.py`.
