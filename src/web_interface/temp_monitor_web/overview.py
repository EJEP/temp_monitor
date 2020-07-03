"""Display a temperature overview as a home page"""
import sqlite3
import datetime
import json
from flask import Flask, render_template, g, Blueprint, current_app, request

from temp_monitor_web.db import get_db


bp = Blueprint('overview', __name__)

def get_min_max(table, func):
    """Return all records from the database after the interval"""

    conn = get_db()
    curs = conn.cursor()
    curs.execute("SELECT measurement_time, " + func + "(temp) FROM " + table + " WHERE measurement_time BETWEEN DATETIME('now', '-72 hours') AND DATETIME('now')" )

    rows = curs.fetchone()

    curs.close()

    return rows

def get_overview(table):
    mint = get_min_max(table, 'min')
    maxt = get_min_max(table, 'max')

    if table == 'owm_temps':
        source = 'OWM'
    elif table == 'metoffice_temps':
        source = 'Met Office'
    elif table == 'sensor_temps':
        source = 'Sensor'
    else:
        source = table

    return {'source': source, 'mint': mint, 'maxt':maxt}


@bp.route('/')
def overview():

    owm_data = get_overview('owm_temps')
    metoffice_data = get_overview('metoffice_temps')
    sensor_data = get_overview('sensor_temps')

    return render_template('overview.html', owm_data=owm_data,
                           metoffice_data=metoffice_data, sensor_data=sensor_data)
