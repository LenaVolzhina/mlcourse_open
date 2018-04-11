import logging
import sys
from datetime import datetime

logging.basicConfig(filename='hw8_data/preprocess_data_log.txt', level=logging.DEBUG)

def log(msg, p=True):
    msg_dt = "[{}] {}".format(datetime.now(), msg)
    if p: print(msg_dt)
    logging.info(msg_dt)


"""Давайте выберем в наших данных все вопросы с тегами javascript, java, python, ruby, php, c++, c#, go, scala и swift и подготовим обучающую выборку в формате Vowpal Wabbit. Будем решать задачу 10-классовой классификации вопросов по перечисленным тегам.
Вообще, как мы видим, у каждого вопроса может быть несколько тегов, но мы упростим себе задачу и будем у каждого вопроса выбирать один из перечисленных тегов либо игнорировать вопрос, если таковых тегов нет. Но вообще VW поддерживает multilabel classification (аргумент --multilabel_oaa). 

Реализуйте в виде отдельного файла preprocess.py код для подготовки данных. Он должен отобрать строки, в которых есть перечисленные теги, и переписать их в отдельный файл в формат Vowpal Wabbit. Детали:
* скрипт должен работать с аргументами командной строки: с путями к файлам на входе и на выходе
* строки обрабатываются по одной (можно использовать tqdm для подсчета числа итераций)
* если табуляций в строке нет или их больше одной, считаем строку поврежденной и пропускаем
в противном случае смотрим, сколько в строке тегов из списка javascript, java, python, ruby, php, c++, c#, go, scala и swift. Если ровно один, то записываем строку в выходной файл в формате VW: label | text, где label – число от 1 до 10 (1 - javascript, ... 10 – swift). Пропускаем те строки, где интересующих тегов больше или меньше одного
из текста вопроса надо выкинуть двоеточия и вертикальные палки, если они есть – в VW это спецсимволы"""

TAGS = ['javascript', 'java', 'python', 'ruby', 'php', 'c++', 'c#', 'go', 'scala', 'swift']


def preprocess(source_filename, target_filename):
    corrupted, bad_tags, ok = 0, 0, 0
    labels = dict(zip(TAGS, range(1, len(TAGS) + 1)))
    log("Labels: " + str(labels))
    with open(target_filename, 'w') as target_file:
        with open(source_filename) as source_file:
            for n, line in enumerate(source_file):
                bad_lines = [3398558, 3890296, 4350090, 5987980]
                if n in bad_lines:
                    log("line #{}: '{}'".format(n, line))
                
                splitted = line.strip().split('\t')
                if len(splitted) != 2:
                    corrupted += 1
                    continue

                text, tags = splitted
                tags = [t.strip() for t in tags.strip().split(' ')]
                good_tags = [t for t in tags if t in TAGS]
                if len(good_tags) != 1:
                    bad_tags += 1
                    continue

                text = text.replace(':', '').replace('|', '')
                label = labels[good_tags[0]]
                target_file.write("{} | {}\n".format(label, text))
                ok += 1

                n += 1
                if n % 10000 == 0:
                    log(n, p=False)

    log("corrupted: {}, bad tags: {}, ok lines: {}".format(corrupted, bad_tags, ok))


if __name__ == '__main__':
    print(sys.argv)
    preprocess(sys.argv[1], sys.argv[2])



