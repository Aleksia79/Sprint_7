from allure import title, step
from src.config import Config


class TestAcceptOrder:

    @title('Проверка принятия заказа при запросе с корректными id заказа и id курьера')
    def test_accept_order(self, get_order_id, create_courier_and_return_object, accept_order_api):
        order_id = get_order_id
        courier = create_courier_and_return_object
        courier_id = courier.courier_id
        with step(f'Передаем на ручку {Config.ACCEPT_ORDER} id заказа: {order_id}; и id курьера: {courier_id}'):
            response = accept_order_api.accept_order(order_id, courier_id)
        with step('ОР: Код ответа 200'):
            assert response.status_code == 200
        with step('ОР: В теле ответа: {"ok": True}'):
            assert response.json() == {"ok": True}

    @title('Проверка принятия заказа при запросе с корректными id заказа и без id курьера')
    def test_accept_order_no_courier_id(self, get_order_id, accept_order_api):
        order_id = get_order_id
        with step(f'Передаем на ручку {Config.ACCEPT_ORDER} id заказа: {order_id}; и id курьера: ""'):
            response = accept_order_api.accept_order(order_id, "")
        with step('ОР: Код ответа 400'):
            assert response.status_code == 400
        with step('ОР: В теле ответа: {"message": "Недостаточно данных для поиска"}'):
            assert response.json() == {"message": "Недостаточно данных для поиска"}

    @title('Проверка принятия заказа при запросе с корректными id курьера и без id заказа')
    def test_accept_order_no_order_id(self, create_courier_and_return_object, accept_order_api):
        courier = create_courier_and_return_object
        courier_id = courier.courier_id
        with step(f'Передаем на ручку {Config.ACCEPT_ORDER} id заказа: ""; и id курьера: {courier_id}'):
            response = accept_order_api.accept_order("", courier_id)
        with step('ОР: Код ответа 400'):
            assert response.status_code == 400
        with step('ОР: В теле ответа: {"message": "Недостаточно данных для поиска"}'):
            assert response.json() == {"message": "Недостаточно данных для поиска"}

    @title('Проверка принятия заказа при запросе с несуществующим id курьера')
    def test_accept_order_incorrect_courier_id(self, get_order_id, create_courier_and_return_object, accept_order_api):
        order_id = get_order_id
        courier = create_courier_and_return_object
        courier_id = courier.courier_id
        with step(f'Удаляем курьера с id {courier_id}'):
            courier.delete_courier_by_id(courier_id)
        with step(f'Передаем на ручку {Config.ACCEPT_ORDER} id заказа: {order_id}; и id удаленного курьера:'
                  f' {courier_id}'):
            response = accept_order_api.accept_order(order_id, courier_id)
        with step('ОР: Код ответа 404'):
            assert response.status_code == 404
        with step('ОР: В теле ответа: {"message": "Курьера с таким id не существует"}'):
            assert response.json() == {"message": "Курьера с таким id не существует"}

    @title('Проверка принятия заказа при запросе с несуществующим id заказа')
    def test_accept_order_incorrect_order_id(self, create_order_and_object, create_courier_and_return_object,
                                             accept_order_api):
        order = create_order_and_object
        order_id = order.order_body.json()["order"]["id"]
        courier = create_courier_and_return_object
        courier_id = courier.courier_id
        with step(f'Передаем на ручку {Config.ACCEPT_ORDER} несуществующий id заказа: ({order_id} - 1); и id '
                  f'курьера: {courier_id}'):
            response = accept_order_api.accept_order(order_id - 1, courier_id)
        with step('ОР: Код ответа 404'):
            assert response.status_code == 404
        with step('ОР: В теле ответа: {"message": "Заказа с таким id не существует"}'):
            assert response.json() == {"message": "Заказа с таким id не существует"}
