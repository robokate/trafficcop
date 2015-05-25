__author__ = 'kate'

from wtforms import Form, StringField, validators

class ShortenForm(Form):
    url_to_shorten = StringField('Url to Shorten',\
                                 [validators.DataRequired(message=u'You must enter a url to shrink.')])