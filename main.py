import sys
import unittest
from unittest.mock import patch

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def print_name(request, doc=documents):
    # request = input('Введите номер документа: ')
    for el in doc:
        if el['number'] == request:
            # print(el['name'])
            return el['name']
        else:
            continue
    res = 'Документ с указанным номером отсутствует.'
    return res


def search_shelf(number, my_dir=directories):
    available = False
    # number = input('Введите номер документа: ')
    for el in my_dir.values():
        if number in el:
            available = True
            break

    if available:
        for shelf, num in my_dir.items():
            for i in num:
                if i == number:
                    res = f'Документ номер {number} на полке {shelf}.'
                    return res
    else:
        res = 'Документ с указанным Вами номером не существует.'
        return res


def print_list(doc=documents):
    res = ''
    count = 0
    for list_doc in doc:
        for el in list_doc.values():
            res += el + ' '
            count += 1
            if count == 3:
                res = res.rstrip()
                res += '\n'
                count = 0
    return res


def add_doc(data, person, number_doc, number_shelf, doc=documents, my_dir=directories):
    my_list = [i for i in my_dir]
    my_str = ''
    count = 0
    for i in my_list:
        if count != len(my_list) - 1:
            my_str += i + ', '
            count += 1
        else:
            my_str += i

    # data = input('Введите тип документа (например passport): ')
    # person = input('Введите имя владельца: ')
    # number_doc = input('Введите номер документа: ')
    # number_shelf = input(f'Введите номер полки, на которую хотите поместить досье (выберите из списка - {my_str}): ')

    if number_shelf not in my_dir:
        res = 'Выбранная Вами полка не существует. Повторите вызов команды и выберите полку из предложенного списка.'
        return res
    else:
        doc.append({'type': data, 'number': number_doc, 'name': person})
        my_dir[number_shelf].append(number_doc)
        # res = 'Введенные Вами данные успешно добавлены.'
        return doc


def del_doc(number, doc=documents, my_dir=directories):
    available = False
    # number = input('Введите номер документа подлежащего удалению: ')
    for el in my_dir.values():
        if number in el:
            available = True
            break

    if available:
        end = False
        for shelf, num in my_dir.items():
            if end:
                break
            for i in num:
                if i == number:
                    my_dir[shelf].remove(number)
                    # print(f'Документ номер {number} удален с полки {shelf}.')
                    end = True
                    break
        for el in doc:
            if el['number'] == number:
                doc.remove(el)
                return my_dir
    else:
        res = 'Документ с указанным Вами номером не существует.'
        return res


def move_doc(shelf, number, doc=documents, my_dir=directories):
    available = False
    old_shelf = ''
    # shelf = input('Введите номер полки, на которую Вы хотите переместить документ: ')
    # number = input('Введите номер документа, который необходимо переместить: ')

    if shelf not in my_dir:
        res = 'Указанная Вами полка отсутствует.'
        return res
    for sh, num in my_dir.items():
        if number in num:
            available = True
            old_shelf = sh
            break

    if available:
        my_dir[shelf].append(number)
        my_dir[old_shelf].remove(number)
        res = f'Документ {number} перемещен на полку {shelf}.'
        return res
    else:
        res = 'Указанный Вами документ отсутствует.'
        return res


def add_shelf(shelf, my_dir=directories):
    # shelf = input('Введите номер полки, которую хотите добавить: ')

    if shelf in my_dir:
        res = 'Такая полка уже существует.'
        return res
    else:
        my_dir[shelf] = []
        res = f'Полка номер {shelf} успешно добавлена.'
        return res


def error():
    res = 'Введенная Вами команда не существует.'
    return res


text = '''Для работы с документами Вам доступны следующие команды:
	p – people - команда, которая спросит номер документа и выведет имя человека, которому он принадлежит
	s – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится
	l– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин"
	a – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться.
	d – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок.
	m – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую
	as – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень.
	q - quit - команда, которая завершит работу программы
	h - help - повторно выведет данное меню '''

comm_dict = {
    'p': print_name,
    's': search_shelf,
    'l': print_list,
    'a': add_doc,
    'd': del_doc,
    'm': move_doc,
    'as': add_shelf,
    'q': sys.exit,
    'h': lambda: print(text)
}

# print(text)
# while True:
#     print()
#     command = input('Введите команду: ')
#     command = command.lower().strip()
#     comm_dict.get(command, error)()
