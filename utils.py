import os
from collections import defaultdict
from database import db, TfTable, IdfTable
import math


def get_files():
    return os.listdir('uploads')


def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def clean_string(my_string):
    import string
    table = str.maketrans('', '', string.punctuation)
    return my_string.lower().translate(table)


def count_words(filename):
    file_name = filename.split('/')[-1]
    word_counts = defaultdict(int)
    with open('uploads/' + filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = clean_string(line)
            words = line.split()
            for word in words:
                word_counts[word] += 1

    for word in word_counts:
        query = TfTable(word=word, tf=0, file_name=file_name)
        db.session.add(query)
    db.session.commit()
    res = {'file_name': file_name, 'word_counts': word_counts}
    return res


def calculate_tf(data):
    tf = {}
    for word, count in data['word_counts'].items():
        tf[word] = round(count / sum(data['word_counts'].values()), 3)
        db.session.query(TfTable).filter_by(word=word, file_name=data['file_name']).update({'tf': tf[word]})
    db.session.commit()


def calculate_idf(data):
    idf = {}
    num_documents = len(get_files())
    for word in data['word_counts']:
        count_in_files = db.session.query(TfTable).filter_by(word=word).count()
        if count_in_files == 0:
            count_in_files = 1
        idf[word] = round(math.log(num_documents / count_in_files, 10), 3)
        if db.session.query(IdfTable).filter_by(word=word).count() == 0:
            query = IdfTable(word=word, idf=idf[word])
            db.session.add(query)
        else:
            db.session.query(IdfTable).filter_by(word=word).update({'idf': idf[word]})
    db.session.commit()


def make_it_simple():
    info = {}
    idf_data = db.session.query(IdfTable).all()
    for idf in idf_data:
        tf = db.session.query(TfTable).filter_by(word=idf.word).first()
        info[idf.word] = {'tf': tf.tf, 'idf': idf.idf}
    info = sorted(info.items(), key=lambda x: x[1]['idf'], reverse=True)
    return info
