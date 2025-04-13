from allure import title, step
import requests

from src.config import Config


class OrdersApi:

    def __init__(self, url_endpoint, order_track=None, order_body=None, response=None):
        self.url_endpoint = url_endpoint
        self.order_track = order_track
        self.order_body = order_body
        self.response = response

    @title('Создаем заказ и присваиваем объекту номер трека и информацию о заказе по треку')
    def create_order(self, order_body):
        with step('Отправляем POST-запрос с телом заказа на создание заказа'):
            self.response = requests.post(self.url_endpoint, json=order_body)
        self.order_track = self.response.json()
        with step(f'Получаем track-номер: {self.order_track["track"]}'):
            self.order_body = self.get_order_by_track(self.order_track["track"])
        return self.response

    @title('Получаем список заказов')
    def get_list_orders(self):
        with step('Отправляем GET-запрос на получение списка заказов'):
            response = requests.get(self.url_endpoint)
        return response

    @title('Принимаем заказ')
    def accept_order(self, order_id, courier_id):
        payload = {}
        if courier_id is not None:
            payload = {'courierId': f'{courier_id}'}
        with step(f'Отправляем PUT-запрос на принятие заказа с параметрами: id заказа {order_id} и courierId {courier_id}'):
            response = requests.put(f'{Config.URL + Config.ACCEPT_ORDER}{order_id}', params=payload)
        return response

    @title('Получаем заказ по его треку')
    def get_order_by_track(self, track):
        payload = {'t': f'{track}'}
        with step('Отправляем GET-запрос с параметром t (track) на получение информации о заказе'):
            response = requests.get(f'{Config.URL + Config.ORDER_TRACK}', params=payload)
        return response

    def destroy(self):
        if self.order_track is not None:
            with step(f'Отмена заказа с треком {self.order_track}'):
                response = requests.put(f'{Config.URL + Config.CANCEL_ORDER}', json=self.order_track)
            with step(f'Запрос на отмену заказа выполнен со статус-кодом: {response.status_code}'):
                pass
            return response
        with step('Заказ не найден'):
            pass

    def cancel_order_by_track(self, order_track):
        with step(f'Отмена заказа с треком {order_track}'):
            response = requests.put(f'{self.url_endpoint}/cancel', json=order_track)
        return response

