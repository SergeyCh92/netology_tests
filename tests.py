import unittest
from main import print_name, search_shelf, print_list, add_doc, del_doc
from ya import YaUpLoader

with open('toc_ya.txt') as f:
    token_ya = f.read().strip()


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print('Начало тестов.')

    def setUp(self) -> None:
        self.ya = YaUpLoader(token_ya)
        self.doc = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]
        self.directories = {
            '1': ['2207 876234', '11-2'],
            '2': ['10006'],
            '3': []
        }

    def test_print_name(self):
        self.assertEqual(print_name('11-2'), 'Геннадий Покемонов')

    def test_print_name_two(self):
        self.assertEqual(print_name('10006'), 'Аристарх Павлов')

    def test_search_shelf(self):
        self.assertEqual(search_shelf('11-2'), 'Документ номер 11-2 на полке 1.')

    def test_print_list(self):
        self.assertEqual(print_list(), 'passport 2207 876234 Василий Гупкин\ninvoice 11-2 Геннадий Покемонов\n'
                                       'insurance 10006 Аристарх Павлов\n')

    def test_add_doc(self):
        test_dict = {"type": "passport", "number": "14151", "name": "Иван Иванов"}
        self.assertIn(test_dict,
                      add_doc('passport', 'Иван Иванов', '14151', '3', doc=self.doc, my_dir=self.directories))

    def test_add_doc_negative(self):
        res = 'Выбранная Вами полка не существует. Повторите вызов команды и выберите полку из предложенного списка.'
        self.assertEqual(add_doc('passport', 'Иван Иванов', '14151', '8', doc=self.doc, my_dir=self.directories), res)

    def test_del_doc(self):
        self.assertNotIn('10006', del_doc('10006', doc=self.doc, my_dir=self.directories))

    def test_del_doc_negative(self):
        res = 'Документ с указанным Вами номером не существует.'
        self.assertEqual(del_doc('5454ff654ds', doc=self.doc, my_dir=self.directories), res)

    def test_create_dir(self):  # проверка успешного создания папки на яндекс-диске
        self.assertEqual(201, self.ya.create_dir_vk())
        self.assertIn('Файлы Вк', self.ya.get_list_files())

    # def test_create_dir_access_ban(self):  # проверка ожидаемого кода ответа (401) в случае использования неверного токена
    #     self.assertEqual(401, self.ya.create_dir_vk())

    @classmethod
    def tearDownClass(cls) -> None:
        print('Завершение тестов.')


if __name__ == '__main__':
    unittest.main()
