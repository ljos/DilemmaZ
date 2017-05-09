from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class Article(FlaskForm):

    msg = """1. prevention of harm of owner/user
2. prevention of harm to people
3. prevention of harm to animal
4. prevention of harm to property
5. prevent harm by external causes
6. Respect for autonomy
7. Fidelity, truth telling"""


    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])

    dilemma_body = TextAreaField('Dilemma Body', validators=[DataRequired()])

    article_url = StringField('Article URL', validators=[DataRequired()])


    logic = TextAreaField('Logic', validators=[])


    feature = TextAreaField('Feature', validators=[], default=msg)

    actions = TextAreaField('Actions', validators=[])

    case = TextAreaField('Case', validators=[])

    duty_values = TextAreaField('Duty Values', validators=[])


    submit = SubmitField("Submit")
