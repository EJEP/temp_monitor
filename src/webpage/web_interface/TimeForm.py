from flask_wtf import FlaskForm
from wtforms import SelectField

class TimeForm(FlaskForm):
    """Class to manage the generation of the time selection form"""

    # Choices is a sequence of (value, label) pairs
    the_time = SelectField(u'Time range',
                           choices = [('last6', 'The last 6 hours'),
                                      ('last12', 'The last 12 hours'),
                                      ('last24', 'The last 24 hours'),
                                      ('last48', 'The last 48 hours'),
                                      ('last72', 'The last 72 hours'),
                                      ('last168', 'The last 168 hours'),
                                      ('all', 'All records')])
