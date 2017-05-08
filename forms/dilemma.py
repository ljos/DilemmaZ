from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class Dilemma(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    dilemma = TextAreaField('dilemma', validators=[DataRequired()])
    submit = SubmitField("Submit")
