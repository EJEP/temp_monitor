"""Use flask to display the data on a web page"""

import sqlite3
import datetime
from bokeh.plotting import figure
from bokeh.embed import json_item, components
from bokeh.resources import CDN
import json
from flask import Flask, render_template
from jinja2 import Template

import config
from TimeForm import TimeForm

app = Flask(__name__)

page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>
<body>
  <div id="myplot"></div>
  <script>
  fetch('/plot')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item); })
  </script>
</body>
""")


def get_data(table, interval):
    """Return all records from the database after the interval"""

    conn=sqlite3.connect(config.DBNAME, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM " + table)
    else:
        curs.execute("SELECT * FROM " + table + " WHERE time>datetime('now','-%s hours')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows

@app.route('/plot')
def plot_data():
    """Plot the data in Bokeh"""

    option = None
    # get sensor data from the database
    sensor_records=get_data('sensor_temps', option)

    # get weather data
    owm_records=get_data('owm_temps', option)

    # get metoffice data
    met_records=get_data('metoffice_temps', option)

    p = figure(plot_width=800, plot_height=500, x_axis_type="datetime")

    p.line([s[0] for s in sensor_records], [s[1] for s in sensor_records], color='blue',
           legend='sensor')
    p.line([o[0] for o in owm_records], [o[1] for o in owm_records], color='red',
           legend='OWM')
    p.line([m[0] for m in met_records], [m[1] for m in met_records], color='black',
           legend='MetOffice')

    # Jsonify the plot to put in html
    plot_text = json.dumps(json_item(p, 'myplot'))
    #plot_script, plot_div = components(p)

    #return plot_script, plot_div
    return plot_text

def plot_data_2():
    """Plot the data in Bokeh"""

    option = None
    # get sensor data from the database
    sensor_records=get_data('sensor_temps', option)

    # get weather data
    owm_records=get_data('owm_temps', option)

    # get metoffice data
    met_records=get_data('metoffice_temps', option)

    p = figure(plot_width=800, plot_height=500, x_axis_type="datetime")

    p.line([s[0] for s in sensor_records], [s[1] for s in sensor_records], color='blue',
           legend='sensor')
    p.line([o[0] for o in owm_records], [o[1] for o in owm_records], color='red',
           legend='OWM')
    p.line([m[0] for m in met_records], [m[1] for m in met_records], color='black',
           legend='MetOffice')

    # Jsonify the plot to put in html
    plot_script, plot_div = components(p)

    return plot_script, plot_div

@app.route('/the_plot', methods=['GET', 'POST'])
def hello():

    time_chooser = TimeForm()

    plot_script, plot_div = plot_data_2()
    # CDN.render() has all of the information to get the javascript libraries
    # for Bokeh to work, loaded from a cdn somewhere.
    return render_template('temp_graph.html', plot_div=plot_div,
                           plot_script=plot_script, resources=CDN.render())
    #return page.render(resources=CDN.render())
