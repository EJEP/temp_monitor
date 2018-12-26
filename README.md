# Monitor temperature #

Monitor temperature from a sensor and display on a webpage

## Monitor Script ##

This script reads the temperature from a DS18B20 temperature sensor and two weather services (OpenWeatherMap and the Met Office) and stores all the information in a database.

### Requirements ###

+ SQLite
+ [pyowm](https://github.com/csparpa/pyowm)
+ [metoffer](https://github.com/sludgedesk/metoffer)
+ [w1thermsensor](https://github.com/timofurrer/w1thermsensor)

API keys are required for the [OpenWeatherMap API](https://openweathermap.org/api) and the MetOffice [Datapoint API](https://www.metoffice.gov.uk/datapoint).

### Setup ###

Database configuration. Needs tables for the sensor and the two weather services with fields/columns for the time and temperature.

### Configuration ###

The configuration is done in `config.py`. This stores the API keys and the coordinates of the location for the weather.

The variables in `config.py` are:

+ `OWM_API_KEY`: The API key for OpenWeatherMap.
+ `DATAPOINT_API_KEY`: The API key for datapoint.
+ `COORDS`: The coordinates to use for the weather reporting, in decimal latitude/longitude.


## Web Page ## 

The web page shows the temperature on a graph using [Bokeh](https://bokeh.pydata.org/en/latest/). [Flask](http://flask.pocoo.org/) is used to display the page.

### Requirements ###

+ [Bokeh](https://bokeh.pydata.org/en/latest/)
+ [Flask](http://flask.pocoo.org/)
+ [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
+ [WTForms](https://wtforms.readthedocs.io/en/stable/)

### Configuration ###

To come...

The web page is written
