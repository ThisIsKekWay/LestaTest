import os

from flask import Flask, render_template, request

from form import TxtFileForm
from config import Config
from utils import count_words, calculate_tf, calculate_idf, make_it_simple, check_dir, get_files
from database import db, init_db, TfTable, IdfTable

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_PATH
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

with app.app_context():
    check_dir(app.config['UPLOAD_FOLDER'])
    init_db()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = TxtFileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.file.data
            if file:
                filename = file.filename
                if filename not in get_files():
                    file.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
                    words_dict = count_words(filename)
                    calculate_tf(words_dict)
                    calculate_idf(words_dict)
                    res = make_it_simple()
                else:
                    words_dict = count_words(filename)
                    res = make_it_simple()
                return render_template('stat_table.html', data=res, files=get_files())
    return render_template('index.html', form=form, files=get_files())


@app.route('/stat', methods=['GET'])
def stat():
    res = make_it_simple()
    return render_template('stat_table.html', data=res, files=get_files())


@app.route('/drop', methods=['GET'])
def drop():
    load_dir = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(load_dir):
        file_path = os.path.join(load_dir, filename)
        os.remove(file_path)
    db.session.query(TfTable).delete()
    db.session.query(IdfTable).delete()
    db.session.commit()
    return render_template('index.html', form=TxtFileForm(), files=get_files())


if __name__ == '__main__':
    app.run()
