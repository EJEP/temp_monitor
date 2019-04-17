"""Log the temperature from a DS18B20 temperature sensor, and two weather services"""

import sqlite3

import os
import time
import datetime
from time import sleep
import sys

import serial
from w1thermsensor import W1ThermSensor
import pyowm
#import metoffer
import datapoint

import config

def log_temperature(table, time_now, temp):
    """Store the temperature from the DS18B20 in the database.

    Parameters
    ----------

    table: string, the table to insert the data into
    time_now: datetime object, The time of the measurement
    temp: The temperature measured"""

    conn=sqlite3.connect(config.DBNAME)
    curs=conn.cursor()

    curs.execute('INSERT INTO ' + table + ' values(?, ?)', (time_now, temp))

    # commit the changes
    conn.commit()
    conn.close()

def get_sensor():
    """Return the temperature from the DS18B20 sensor"""

    # Use the W1ThermSensor library to communicate with the DS18B20
    sensor = W1ThermSensor()

    # get the temperature from the device file
    sensor_temp = sensor.get_temperature()
    if sensor_temp == None:
        # Sometimes reads fail on the first attempt
        # so we need to retry
        sensor_temp = sensor.get_temperature()

    return sensor_temp

def get_owm():
    """Return the temperature from OWM"""

    # Get temperature from open weather map
    owm = pyowm.OWM(config.OWM_API_KEY)

    # Try the connection up to 10 times
    # This connection retrying is a bit sketchy. Could do with re-writing
    max_retries = 10

    con_error = None
    for i in range(max_retries):
        try:
            observation = owm.weather_at_coords(*config.COORDS_OWM)
            con_error = None
            owm_w = observation.get_weather()

            owm_temp = owm_w.get_temperature('celsius')

            return owm_temp["temp"]

        except pyowm.exceptions.api_call_error.APICallError as con_error:
            t, v, tb = sys.exc_info()
            print('owm try ' + str(i) + ' failed')
            sleep(5)
            pass

        else:
            break
    else:
        print(max_retries)
        #raise t, v, tb
        print(sys.exc_info())

def get_metoffice():
    """Return the temperature from the metoffice"""

    # Get temperature from met office
    conn = datapoint.connection(api_key=config.DATAPOINT_API_KEY)

    # Use similar retry code to above. Again, could do with doing properly.
    max_retries = 10

    con_error = None

    for i in range(max_retries):
        try:
            site = conn.get_nearest_site(*config.COORDS_DATAPOINT)

            forecast = conn.get_forecast_for_site(site.id, "3hourly")
            current_timestep = forecast.now()

            return current_timestep.temperature.value

        except datapoint.exceptions.APIException as con_error:
            t, v, tb = sys.exc_info()
            print('datapoint try ' + str(i) + ' failed')
            print('Error message:')
            print(sys.exc_info())
            sleep(5)
            pass

        else:
            break
    else:
        #raise t, v, tb
        print(sys.exc_info())

def main():

    # Assume all the measurements are taken close enough together that
    # they can all have the same time stamp.
    time_now = datetime.datetime.today()

    # Store the sensor temperature in the database
    sensor_temp = get_sensor()
    log_temperature('sensor_temps', time_now, sensor_temp)

    # Log weather reported temperature in database
    owm_temp = get_owm()
    log_temperature('owm_temps', time_now, owm_temp)

    # Log the weather reported by the Met Office
    met_off_temp = get_metoffice()
    log_temperature('metoffice_temps', time_now, met_off_temp)


if __name__=="__main__":
    main()
