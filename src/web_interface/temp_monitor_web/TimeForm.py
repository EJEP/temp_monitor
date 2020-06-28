from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.fields.html5 import DateTimeField

class TimeForm(FlaskForm):
    """Class to manage the generation of the time selection form"""

    # Choices is a sequence of (value, label) pairs
    # WTForms treats data as a string unless told otherwise, and then fails to
    # validate if the values in choices are not strings. It is possible to tell
    # WTForms that the data it gets are ints (or whatever), but for my purposes
    # strings are more useful
    the_time = SelectField(u'Time range',
                           choices = [('6', 'The last 6 hours'),
                                      ('12', 'The last 12 hours'),
                                      ('24', 'The last 24 hours'),
                                      ('48', 'The last 48 hours'),
                                      ('72', 'The last 72 hours'),
                                      ('168', 'The last 168 hours'),
                                      ('all', 'All records')])
class TimeFormRange(FlaskForm):
    """Class to manage time range input"""

    datetime_1 = DateTimeField(u'Time 1')
    datetime_2 = DateTimeField(u'Time 2')
