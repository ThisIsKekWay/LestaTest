from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from form import TxtFileForm
from utils import create_report, check_dir

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_super_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = TxtFileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.file.data
            if file:
                filename = file.filename
                check_dir(app.config['UPLOAD_FOLDER'])
                file.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
                res = create_report(app.config['UPLOAD_FOLDER'] + '/' + filename)
                return render_template('stat_table.html', data=res)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
