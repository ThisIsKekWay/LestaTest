from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField


class TxtFileForm(FlaskForm):
    file = FileField('Файл', validators=[FileRequired(), FileAllowed(['txt'], 'Только txt')])
    submit = 'Загрузить'
