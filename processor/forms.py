
from wtforms import StringField, Form
from wtforms.validators import required


class gramsForm(Form):
    """ grams Form """
    phrases = StringField('phrases :', [required()])