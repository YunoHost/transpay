from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

projectNameValidators = [DataRequired()]
projectIdValidators = [DataRequired()]

class NewProjectForm(FlaskForm):
    name = StringField(validators=projectNameValidators)

class ProjectForm(FlaskForm):
    name = StringField(validators=projectNameValidators)
    id = HiddenField(validators=projectIdValidators)

class DeleteProjectForm(FlaskForm):
    id = HiddenField(validators=projectIdValidators)
