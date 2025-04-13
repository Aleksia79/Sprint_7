from allure import title, step
import pytest

from src.config import Config
from src.data import Data
from src.courier_api import CourierApi
from src.helpers import generate_courier_data
from src.orders_api import OrdersApi


@pytest.fixture()
@title('Создаем объект курьер')
def courier_api():
    courier = CourierApi(Config.URL)
    yield courier
    with step('Удаляем курьера'):
        courier.destroy()


@pytest.fixture()
@title(f'Добавляем к URL {Config.URL} ручку {Config.ORDERS}')
def orders_api():
    order = OrdersApi(Config.URL + Config.ORDERS)
    yield order
    with step('Удаляем заказ'):
        order.destroy()


@pytest.fixture()
@title(f'Добавляем к URL {Config.URL} ручку {Config.ACCEPT_ORDER}')
def accept_order_api():
    return OrdersApi(Config.URL + Config.ACCEPT_ORDER)


@pytest.fixture()
@title('Генерируем данные курьера, регистрируем и возвращаем объект - курьер с id')
def create_courier_and_return_object(courier_api):
    with step('Генерируем login, password, first_name курьера'):
        login, password, first_name = generate_courier_data()
    courier = courier_api
    with step('Создаем курьера по сгенерированным login, password, first_name курьера'):
        courier.create_courier(login, password, first_name)
    with step(f'Получили id курьера: {courier.courier_id}'):
        return courier


@pytest.fixture()
@title('Создаем заказ и объект')
def create_order_and_object(orders_api):
    order = orders_api
    order.create_order(Data.order_body)
    return order


@pytest.fixture()
@title('Получаем id заказа по треку')
def get_order_id(orders_api, create_order_and_object):
    data_order = create_order_and_object
    order_id = data_order.order_body.json()["order"]["id"]
    with step(f'Получили id заказа: {order_id}'):
        return order_id
