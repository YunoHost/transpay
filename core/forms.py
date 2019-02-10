from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired

projectNameValidators = [DataRequired()]
projectIdValidators = [DataRequired()]

class NewProjectForm(FlaskForm):
    name = StringField(validators=projectNameValidators)

class DeleteProjectForm(FlaskForm):
    id = HiddenField(validators=projectIdValidators)

class ProjectForm(FlaskForm):
    name = StringField(validators=projectNameValidators)
    id = HiddenField(validators=projectIdValidators)

    def __init__(self, *args, **kwargs):
        if 'project' in kwargs:
            project = kwargs['project']
            FlaskForm.__init__(self, name=project.name, id=project.id, *args, **kwargs)
            self.nametext = project.name
            self.donations = project.donations
            self.delform = DeleteProjectForm(id=project.id)
        else:
            FlaskForm.__init__(self, *args, **kwargs)

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
