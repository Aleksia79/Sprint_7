from src.data import Data
from allure import title, step


class TestGetOrderByTrack:

    @title('Проверка на получение заказа при передаче существующего трека')
    def test_get_order_by_track(self, create_order_and_object):
        order = create_order_and_object
        result = order.order_body.json()
        response = order.get_order_by_track(result["order"]["track"])
        with step('ОР: Код ответа 200'):
            assert response.status_code == 200
        with step('ОР: Запрос возвращает объект с заказом'):
            assert "order" in result.keys()
        with step('ОР: в теле ответа в поле "firsName" значение "Naruto"'):
            assert result["order"]["firstName"] == "Naruto"
        with step('ОР: в теле ответа в поле "address" значение "Konoha, 142 apt."'):
            assert result["order"]["address"] == "Konoha, 142 apt."
        with step('ОР: в теле ответа в поле "phone" значение "+7 800 355 35 35"'):
            assert result["order"]["phone"] == "+7 800 355 35 35"

    @title('Проверка на получение заказа при передаче запроса без трека')
    def test_get_order_no_track(self, orders_api):
        with step('Передаем запрос без трекингового номера'):
            response = orders_api.get_order_by_track("")
        with step('ОР: Код ответа 400'):
            assert response.status_code == 400
        with step('ОР: в теле ответа {"message":  "Недостаточно данных для поиска"}'):
            assert response.json() == {"message":  "Недостаточно данных для поиска"}

    @title('Проверка на получение заказа при передаче несуществующего трека')
    def test_get_order_non_existent_track(self, orders_api):
        with step('Передаем запрос с несуществующим трекинговым номером'):
            response = orders_api.get_order_by_track(1000000000)
        with step('ОР: Код ответа 404'):
            assert response.status_code == 404
        with step('ОР: в теле ответа {"message":  "Заказ не найден"}'):
            assert response.json() == {"message": "Заказ не найден"}
