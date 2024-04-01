import os
from collections import defaultdict


def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def clean_string(my_string):
    """
    Очистить строку от знаков препинания и привести к нижнему регистру
    :param my_string:
    :return:
    """
    import string
    table = str.maketrans('', '', string.punctuation)
    return my_string.lower().translate(table)


def create_report(filename):
    word_counts = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = clean_string(line)
            words = line.split()
            for word in words:
                word_counts[word] += 1

    tf = {}
    for word, count in word_counts.items():
        tf[word] = round(count / len(words), 2)

    idf = {}
    num_documents = len(os.listdir('uploads'))
    for word in word_counts:
        idf[word] = round(num_documents / (1 + word_counts[word]), 2)

    data = {}
    for word in word_counts:
        data[word] = {'tf': tf[word], 'idf': idf[word], 'tf_idf': round(tf[word] * idf[word], 2)}
    data = sorted(data.items(), key=lambda x: x[1]['idf'], reverse=True)
    return data
