from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class Article(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[DataRequired()])
    dilemma_body = TextAreaField('Dilemma Body', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    article_url = StringField('Article URL', validators=[DataRequired()])
    submit = SubmitField("Submit")
