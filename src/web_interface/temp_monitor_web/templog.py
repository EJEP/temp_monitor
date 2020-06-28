"""Use flask to display temperature data from a temperature sensor and weather
forecasts on a web page"""

import sqlite3
import datetime
from bokeh.plotting import figure
from bokeh.embed import json_item, components
from bokeh.resources import CDN
from bokeh.models import HoverTool, Legend
import json
from flask import Flask, render_template, g, Blueprint, current_app, request

from temp_monitor_web.db import get_db

from . import TimeForm

bp = Blueprint('plots', __name__)

def get_data(table, interval):
    """Return all records from the database after the interval"""

    conn = get_db()
    curs = conn.cursor()

    if interval == 'all':
        curs.execute("SELECT * FROM " + table)
    else:
        curs.execute("SELECT * FROM " + table + " WHERE measurement_time>datetime('now','-%s hours')" % interval)

    rows=curs.fetchall()

    curs.close()

    return rows


def get_data_range(table, dt1, dt2):
    """Return all records from the database after the interval"""

    conn = get_db()
    curs = conn.cursor()
    print(dt1)
    print(type(dt1))
    curs.execute("SELECT * FROM " + table + " WHERE measurement_time BETWEEN '%s' AND '%s'" % (dt1, dt2))

    rows = curs.fetchall()

    curs.close()

    return rows

def make_plot(time_range):
    """Plot the data in Bokeh"""

    # get sensor data from the database
    sensor_records=get_data('sensor_temps', time_range)

    # get weather data
    owm_records=get_data('owm_temps', time_range)

    # get metoffice data
    met_records=get_data('metoffice_temps', time_range)

    p = figure(plot_width=800, plot_height=500, x_axis_type="datetime",
               toolbar_location="above")

    p.add_tools(HoverTool(
        tooltips = [
            ('date', '@x{%Y-%m-%d %H:%M}'),
            ('temp', '$y'),
        ],
        formatters = {
            'x': 'datetime',
        },

       ))

    sensl = p.line([s[0] for s in sensor_records],
                   [s[1] for s in sensor_records],
                   color='#006ba4', line_width=2)

    owml = p.line([o[0] for o in owm_records],
                  [o[1] for o in owm_records],
                  color='#ff800e', line_width=2)

    metl = p.line([m[0] for m in met_records],
                  [m[1] for m in met_records],
                  color='#ababab', line_width=2)

    # The legend will be outside the plot, and so must be defined directly
    leg = Legend(items=[
        ("Sensor", [sensl]),
        ("OWM", [owml]),
        ("MetOffice", [metl]),
    ], location=(5, 360))

    p.add_layout(leg, 'right')

    # Jsonify the plot to put in html
    plot_script, plot_div = components(p)

    return plot_script, plot_div

def make_range_plot(dt1, dt2):
    """Plot the data in Bokeh"""

    # get sensor data from the database
    sensor_records = get_data_range('sensor_temps', dt1, dt2)

    # get weather data
    owm_records = get_data_range('owm_temps', dt1, dt2)

    # get metoffice data
    met_records = get_data_range('metoffice_temps', dt1, dt2)

    p = figure(plot_width=800, plot_height=500, x_axis_type="datetime",
               toolbar_location="above")

    p.add_tools(HoverTool(
        tooltips=[
            ('date', '@x{%Y-%m-%d %H:%M}'),
            ('temp', '$y'),
        ],
        formatters={
            'x': 'datetime',
        },
    ))

    sensl = p.line([s[0] for s in sensor_records],
                   [s[1] for s in sensor_records],
                   color='#006ba4', line_width=2)

    owml = p.line([o[0] for o in owm_records],
                  [o[1] for o in owm_records],
                  color='#ff800e', line_width=2)

    metl = p.line([m[0] for m in met_records],
                  [m[1] for m in met_records],
                  color='#ababab', line_width=2)

    # The legend will be outside the plot, and so must be defined directly
    leg = Legend(items=[
        ("Sensor", [sensl]),
        ("OWM", [owml]),
        ("MetOffice", [metl]),
    ], location=(5, 360))

    p.add_layout(leg, 'right')

    # Jsonify the plot to put in html
    plot_script, plot_div = components(p)

    return plot_script, plot_div


@bp.route('/the_plot', methods=['GET', 'POST'])
def show_plot():

    time_chooser = TimeForm.TimeForm(request.form)

    # By default show the last 72 hours of data
    interval = '72'

    if time_chooser.validate_on_submit():
        #if time_chooser.the_time.data != 'all':
        interval = time_chooser.the_time.data
        current_app.logger.info('interval is %s', interval)
    current_app.logger.info('interval is %s', interval)

    plot_script, plot_div = make_plot(interval)
    # CDN.render() has all of the information to get the javascript libraries
    # for Bokeh to work, loaded from a cdn somewhere.
    return render_template('temp_graph.html', plot_div=plot_div,
                           plot_script=plot_script, resources=CDN.render(),
                           form=time_chooser)

@bp.route('/range_plot', methods=['GET', 'POST'])
def show_range_plot():

    time_chooser = TimeForm.TimeFormRange(request.form)
    # %Y-%m-%d %H:%M:%S
    datetime_1 = '2020-06-01 00:00:00'
    datetime_2 = '2020-06-02 00:00:00'

    if time_chooser.validate_on_submit():
        # if time_chooser.the_time.data != 'all':
        datetime_1 = time_chooser.datetime_1.data
        datetime_2 = time_chooser.datetime_2.data
        current_app.logger.info('datetime_1 is %s', datetime_1)
        current_app.logger.info('datetime_2 is %s', datetime_2)

    plot_script, plot_div = make_range_plot(datetime_1, datetime_2)
    # CDN.render() has all of the information to get the javascript libraries
    # for Bokeh to work, loaded from a cdn somewhere.
    return render_template('temp_range_graph.html', plot_div=plot_div,
                           plot_script=plot_script, resources=CDN.render(),
                           form=time_chooser)
