from datetime import datetime
from time import time
import csv
import os
import re
import shutil


path_backup = r'C:\Users\Igoryan\Desktop\PyTelegramBot\backup'
path_dictionary = r'C:\Users\Igoryan\Desktop\PyTelegramBot\dictionary'


def save_lib(_dict):
    """
    1. сменить директорию на dictonary
        1.1. Сохранить имеющиеся файлы с добавлением в конец времени в мсек.

    2. в цикле по словарю(длина слова):
        2.1. открываем и загружаем файл из csv
        2.2. из загруженных данных создаем множество
        2.3. добавляем множество по данному циклу ключом к созданному из файла
        2.4. сохраняем обновленное множество как "длина слов.csv"
    """
    # Возможно относительный путь "../CSV_main.csv"
    folder = '\\backup__' + datetime.now().strftime("%d-%m-%Y  %H-%M-%S ") + f'({str(int(time()))})'
    shutil.copytree(path_dictionary, path_backup + folder)
    os.chdir('C:\\Users\\Igoryan\\Desktop\\PyTelegramBot\\dictionary')

    for key in _dict:
        try:
            with open(str(key) + '.csv', mode='r') as file:
                words = csv.reader(file, delimiter=',', lineterminator="\r")
                for word in words:
                    _dict[key].update(word)
                    print(word)
        except FileNotFoundError:
            print(f'Файл: {str(key) + ".csv"} несуществует!!!')
            with open(str(key) + '.csv', mode='w') as file:
                words = csv.writer(file, delimiter=',', lineterminator="\r")
            print(f'Файл: {str(key) + ".csv"} создан!!!')

        #сохраняем словари слов
        with open(str(key) + '.csv', mode='w') as file:
            words = csv.writer(file, delimiter=',', lineterminator="\r")
            for word in _dict[key]:
                words.writerow([word])
                print([word])


def sorted(_set, _dict):

    for word in _set:
        if _dict.get(len(word)) is None:
            _dict[len(word)] = {word}
        else:
            _dict[len(word)].update({word})
    if _dict.get(0) is not None:
        del _dict[0]
    if _dict.get(1) is not None:
        del _dict[1]


def edit(name_file, dt):
    with open(name_file, 'r') as file:
        st = file.read().replace(u'\xa0', ' ').replace(u'.', ' ').replace(u',', ' ')
        st = re.sub('[][()/|^:;*"“„<>»«]', ' ', st)  #/|\\^:;*"?<>.,()-»«
        st = re.sub(r"([АЯ])", r" \1",  st)
        st = st.split(' ')
        dt.update(set(st))
        print(len(dt))


def main():
    os.chdir('C:\\Users\\Igoryan\\Desktop\\PyTelegramBot\\parsing_text\\mk_news')  #директория с тектовыми файлами
    dt = set()
    dt2 = {}

    for file in os.listdir():
        edit(file, dt)
        print(file)
    sorted(dt, dt2)
    save_lib(dt2)


if __name__ == '__main__':
    main()
