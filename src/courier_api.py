from allure import step
import requests
from src.config import Config


class CourierApi:
    @staticmethod
    def login_courier_for_id(login, password):
        courier_data = {"login": login, "password": password}
        id_courier = requests.post(Config.URL + Config.COURIER_LOGIN, json=courier_data)
        return id_courier

    def __init__(self, url_endpoint, courier_id=None, login=None, password=None, first_name=None,
                 response_create=None, response_login=None, courier_login_data=None):
        self.url_endpoint = url_endpoint
        self.courier_id = courier_id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.response_create = response_create
        self.response_login = response_login
        # courier_login_data - используем для проверок авторизациии при неполном наборе ключей
        self.courier_login_data = courier_login_data

    def set_courier_id(self, login, password):
        try:
            self.courier_id = self.login_courier_for_id(login, password).json()["id"]
        except KeyError:
            pass

    @step(f'Отправляем POST-запрос с параметрами "login", "password", "firstName" для создания курьера на ручку '
          f'{Config.CREATE_COURIER}')
    def create_courier(self, login, password, first_name):
        courier_data = {"login": login, "password": password, "firstName": first_name}
        self.response_create = requests.post(self.url_endpoint + Config.CREATE_COURIER, json=courier_data)
        self.login = login
        self.password = password
        self.first_name = first_name
        self.set_courier_id(login, password)
        return self.response_create

    @step('Авторизация курьера')
    def login_courier(self):
        if self.courier_login_data is None:
            self.courier_login_data = {"login": self.login, "password": self.password}
        with step(f'Отправляем POST-запрос с параметрами "login", "password" для авторизации курьера на ручку '
                  f'{Config.COURIER_LOGIN}'):
            self.response_login = requests.post(self.url_endpoint + Config.COURIER_LOGIN, json=self.courier_login_data)
        return self.response_login

    def destroy(self):
        if self.courier_id is not None:
            with step(f'Удаление курьера с id {self.courier_id}'):
                response = requests.delete(f'{self.url_endpoint + Config.DELETE_COURIER}{self.courier_id}')
            with step(f'Запрос на удаление курьера выполнен со статус-кодом: {response.status_code}'):
                pass
            return response
        with step('Курьер не найден'):
            pass

    def delete_courier_by_id(self, id_courier):
        with step(f'Отправляем DELETE-запрос на удаление курьера с id {id_courier} на ручку {Config.DELETE_COURIER}'):
            response = requests.delete(f'{self.url_endpoint + Config.DELETE_COURIER}/{id_courier}')
        self.courier_id = None
        return response
