import json
import requests
import os
from dotenv import load_dotenv

class IPDefiner:
    """Класс для определения текущего ip адреса пользователя"""
    def __init__(self):
        self.url = 'https://api.ipify.org?format=json'

    def getip(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            return data.get('ip')
        else:
            print("Что-то пошло не так при получении IP:", response.status_code)
            return None

class LocationDefinerFromIP:
    """Класс для получения местоположения по определенному ip адресу пользователя"""
    def __init__(self, ip):
        self.ip = ip
        self.url = f'https://ipinfo.io/{self.ip}/geo'

    def getlocation(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка определения локации: {response.status_code}")
            return None

class LoadToYandexDisc:
    """Класс для загрузки местоположения пользователя на Яндекс.Диск"""
    def __init__(self, token):
        self.token = token
        self.ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def createfolder(self, folder):
        """Создание папки на Яндекс.Диск"""
        params = {"path": folder}
        response = requests.put(self.ya_url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f"Папка '{folder}' создана успешно")
        elif response.status_code == 409:
            print(f"Папка '{folder}' уже существует")
        else:
            print(f"Ошибка создания папки: {response.status_code}, {response.text}")

    def uploadyadisc(self, folder, file, data):
        """Загрузка местоположения в формате JSON в созданную папку на Яндекс.Диск"""
        path_to_yadisc = f'{folder}/{file}'
        upload_url = f'{self.ya_url}/upload'
        params = {"path": path_to_yadisc, "overwrite": "true"}

        response = requests.get(upload_url, headers=self.headers, params=params)
        if response.status_code == 200:
            href = response.json().get("href")
            json_data = json.dumps(data, indent=4)
            load_response = requests.put(href, data=json_data)
            if load_response.status_code == 201:
                print(f"Файл '{file}' на Яндекс.Диск загружен успешно")
        else:
            print("Не удалось получить ссылку для загрузки:", response.status_code)

def main():
    load_dotenv()
    token = os.getenv("YANDEX_TOKEN")

    if not token:
        print("Токен Яндекс.Диск не найден в переменных окружения (.env)")
        return

    try:
        ip_finder = IPDefiner()
        current_ip = ip_finder.getip()

        if current_ip:
            location_finder = LocationDefinerFromIP(current_ip)
            location_data = location_finder.getlocation()

            if location_data:
                yandex_disc = LoadToYandexDisc(token)
                folder_name = "My_Location"
                file_name = "location_from_ip.json"
                yandex_disc.createfolder(folder_name)
                yandex_disc.uploadyadisc(folder_name, file_name, location_data)

    except requests.exceptions.ConnectionError:
        print("Ошибка: Отсутствует подключение к интернету.")
    except Exception as err:
        print(f"Произошла непредвиденная ошибка: {err}")

if __name__ == "__main__":
    main()
