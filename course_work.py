import requests
from datetime import datetime
from tqdm import tqdm
import json

with open('TokenVK.txt') as file_object:
    TOKEN_VK = file_object.readline().strip()
    TOKEN_YANDEX = file_object.readline().strip()


class UsersVK:

    def __init__(self, vk_id: str):
        self.vk_id = vk_id
        self.vk_token = TOKEN_VK
        self.url = 'https://api.vk.com/method/'
        self.params = {
            'owner_id': self.vk_id,
            'access_token': self.vk_token,
            'v': '5.131'
        }

    def get_photo(self):
        url_photo = self.url + 'photos.get'
        params = {
            'album_id': 'profile',
            'extended': 'likes',
            'photo_sizes': '1',
            'count': 100
        }
        res = requests.get(url_photo, params={**self.params, **params}).json()

        return res['response']['items']

    def parsed_photo(self, photos_info: list):
        type_sizes = ['w', 'z', 'y', 'x', 'm', 's']
        user_profile_photos = []
        for photo in photos_info:
            photo_dict = {}
            name_photo = str(photo['likes']['count'])
            for user_photo in user_profile_photos:
                if user_photo['name'] == name_photo:
                    name_photo += f"({datetime.utcfromtimestamp(int(photo['date'])).strftime('%Y-%m-%d')})"
            for alpha in type_sizes:
                size = [x for x in photo['sizes'] if x['type'] == alpha]
                type_size = alpha
                if size:
                    break

            photo_dict.setdefault('name', name_photo)
            photo_dict.setdefault('url', size[0]['url'])
            photo_dict.setdefault('type_size', type_size)
            user_profile_photos.append(photo_dict)

        return user_profile_photos


class UsersYD:

    def __init__(self):
        self.token = TOKEN_YANDEX
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def create_folder(self):
        params = {
            'path': '/course_work_by_Gusev_Timur/'
        }
        requests.put(self.url, headers=self.headers, params=params)

    def upload_file(self, files: list):
        upload_url = self.url + 'upload'

        for file in tqdm(files, ascii=True, desc="Загрузка фото: "):
            params_for_upload = {
                'url': file['url'],
                'path': f"course_work_by_Gusev_Timur/{file['name']}",
                'disable_redirects': 'true'
            }
            res = requests.post(upload_url, params=params_for_upload, headers=self.headers)
            status = res.status_code
            with open('data.json', 'a') as outfile:
                json.dump({
                        "file_name": f"{file['name']}.jpg",
                        "size": file['type_size']
                }, outfile, indent=0)
                outfile.write('\n')

        if 400 > status:
            print('Фотографии загружены')
        else:
            print('Ошибка загрузки')


user_vk = UsersVK('223398928')

user_yd = UsersYD()

user_yd.create_folder()
user_yd.upload_file(user_vk.parsed_photo(user_vk.get_photo()))
