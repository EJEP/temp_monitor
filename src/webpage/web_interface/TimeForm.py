from flask_wtf import FlaskForm
from wtforms import SelectField

class TimeForm(FlaskForm):
    """Class to manage the generation of the time selection form"""

    # Choices is a sequence of (value, label) pairs
    the_time = SelectField(u'Time range',
                           choices = [(6, 'The last 6 hours'),
                                      (12, 'The last 12 hours'),
                                      (24, 'The last 24 hours'),
                                      (48, 'The last 48 hours'),
                                      (72, 'The last 72 hours'),
                                      (168, 'The last 168 hours'),
                                      ('all', 'All records')])
