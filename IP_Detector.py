import json
import requests

class IP_Definer:
    """Класс для определения текущего ip адреса пользователя"""
    def __init__(self):
        self.url = 'https://api.ipify.org/?format=json'

    def defining_current_IP(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            return data.get('ip')
        else:
            print("Что-то пошло не так:", response.status_code)
            return None

class Location_Definer_from_IP:
    """Класс для получения местоположения по определенному ip адресу пользователя"""
    def __init__(self, ip):
        self.ip = ip
        self.url = f'https://ipinfo.io/{self.ip}/geo'

    def defining_current_location(self):
        response = requests.get(self.url)
        if response.status_code ==200:
            return response.json()
        else:
            print(f"Ошибка определения локации: {response.status_code}")
            return None

class Load_to_Yandex_Disc:
   """Класс для загрузки местоположения пользователя на Яндекс.Диск"""
   def __init__(self, token):
       self.token = token
       self.ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
       self.headers = {'Authorization': f'OAuth {self.token}'
       }

   def create_folder(self, folder):
       """Создание папки на Яндекс.Диск"""
       params = {"path": folder}
       response = requests.put(self.ya_url, headers=self.headers, params= params)
       if response.status_code == 201:
           print(f"Папка '{folder}' создана успешно")
       elif response.status_code == 409:
           print(f"Папка '{folder}' уже существует")
       else:
           print(f"Ошибка создания папки: {response.status_code}, {response.text}")

   def load_to_yadisc(self, folder, file, data):
       """Загрузка местоположения в формате JSON в созданную папку на Яндекс.Диск"""
       path_to_yadisc = f'{folder}/{file}'
       upload_url = f'{self.ya_url}/upload'
       params = {"path": path_to_yadisc, "overwrite" : "true"}

       # получение ссылки для загрузки
       response = requests.get(upload_url, headers=self.headers, params=params)
       if response.status_code == 200:
           href = response.json().get("href")

           # отправка данных по полученной ссылке
           json_data = json.dumps(data)
           load_response = requests.put(href, data = json_data)
           if load_response.status_code == 201:
               print(f"Файл '{file}' на Яндекс.Диск загружен успешно")
       else:
           print("Не удалось получить ссылку для загрузки:", response.status_code)

if __name__ == "__main__":
    Token = "введите токен"

    # Создание экземпляров классов для определения ip пользователя
    ip_finder = IP_Definer()
    current_ip = ip_finder.defining_current_IP()

    # Создание объекта для поиска местоположения по определенному ip пользователя
    if current_ip:
        location_finder = Location_Definer_from_IP(current_ip)
        location_data = location_finder.defining_current_location()

        # Создание папки и загрузка местоположения в формате JSON на Яндекс.Диск
        if location_data:
            yandex_disc = Load_to_Yandex_Disc(Token)
            folder_name = "My_Location"
            file_name = "location_from_ip.json"
            yandex_disc.create_folder(folder_name)
            yandex_disc.load_to_yadisc(folder_name, file_name, location_data)



















