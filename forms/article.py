from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class Article(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])

    dilemma_body = TextAreaField('Dilemma Body', validators=[DataRequired()])

    article_url = StringField('Article URL', validators=[DataRequired()])


    logic = TextAreaField('Logic', validators=[])


    feature = StringField('Feature', validators=[])

    actions = StringField('Actions', validators=[])

    case = StringField('Case', validators=[])

    duty_values = StringField('Duty Values', validators=[])


    submit = SubmitField("Submit")

