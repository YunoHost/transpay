from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

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
        if "project" in kwargs:
            project = kwargs["project"]
            FlaskForm.__init__(self, name=project.name, id=project.id, *args, **kwargs)
            self.nametext = project.name
            self.donations = project.donations
            self.delform = DeleteProjectForm(id=project.id)
        else:
            FlaskForm.__init__(self, *args, **kwargs)


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()])
    confirm = PasswordField(validators=[DataRequired()])
    token = HiddenField(validators=[DataRequired()])
