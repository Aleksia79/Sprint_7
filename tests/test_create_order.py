from allure import title, step, description
import pytest

from src.data import Data


class TestCreateOrder:

    @title('Проверка поля "color" для успешного создания заказа')
    @description('В параметризованном тесте используем 4 набора тестовых данных: '
                 '  1. В параметр "color" передаем ["BLACK"]'
                 '  2. В параметр "color" передаем ["BLACK", "GREY"]'
                 '  3. В параметр "color" передаем ["GREY"]'
                 '  4. В параметр "color" передаем пустой список []')
    # создание заказа с указанием одного из цветов, с двумя цветами и без указания цвета
    @pytest.mark.parametrize("color", [["BLACK"], ["BLACK", "GREY"], ["GREY"], []])
    def test_create_order_field_color(self, color, orders_api):
        order = orders_api
        Data.order_body["color"] = color
        with step(f'В поле "color" передаем {color}'):
            response = order.create_order(Data.order_body)
        result = response.json()
        with step('ОР: Код ответа на POST-запрос: 201'):
            assert response.status_code == 201
        with step('ОР: Тело ответа на POST-запрос содержит track'):
            assert result.keys() == {"track"}
        with step(f'ОР: В теле ответа на GET-запрос в поле "color" значение {color}'):
            assert order.order_body.json()["order"]["color"] == color
