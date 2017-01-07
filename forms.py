from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField
from wtforms.validators import DataRequired

class CreateEntryForm(FlaskForm):
    subject = StringField('subject', validators=[DataRequired()])
    goal = IntegerField('goal', validators=[DataRequired()])
    comments = StringField('comments', validators=[DataRequired()])
