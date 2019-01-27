from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

projectNameValidators = [DataRequired()]

class NewProjectForm(FlaskForm):
    name = StringField(validators=projectNameValidators)

class ProjectForm(FlaskForm):
    name = StringField(validators=projectNameValidators)
    id = HiddenField(validators=[DataRequired()])
