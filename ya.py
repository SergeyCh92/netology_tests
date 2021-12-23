import requests

with open('toc_ya.txt') as f:
    token_ya = f.read().strip()


class YaUpLoader:
    """Класс создан для взаимодействия с яндекс-диском."""

    def __init__(self, token):
        self.token = token
        self.my_dir = 'Файлы Вк'

    def get_headers(self):
        """Возвращает необходимые заголовки."""
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def _get_upload_link(self, disk_path):
        """Возвращает словарь с информацией о запросе."""
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': disk_path, 'overwrite': 'true'}
        headers = self.get_headers()
        response = requests.get(url=url, params=params, headers=headers, timeout=5)
        # pprint(response.json())
        return response.json()

    def upload_file(self, disk_path, filename):
        """Загружает файлы на яндекс-диск."""
        href = self._get_upload_link(disk_path=disk_path).get('href', '')
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        # if response.status_code == 201:
        #     print(f'Файл {filename} успешно загружен!')

    def create_dir_vk(self):
        """Создает новую папку на яндекс-диске."""
        count = 1
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        while True:
            params = {'path': self.my_dir}
            r = requests.put(url=url, params=params, headers=headers)
            # r.raise_for_status()
            if r.status_code == 409:
                self.my_dir = f'Файлы Вк{count}'
                count += 1
            else:
                return r.status_code

    def get_list_files(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': 'disk:/', 'fields': '_embedded.items.name'}
        r = requests.get(url=url, params=params, headers=headers).json()
        list_data = []
        for el in r['_embedded']['items']:
            list_data.append(el['name'])
        return list_data
