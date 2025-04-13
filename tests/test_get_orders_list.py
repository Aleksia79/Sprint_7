from allure import title, step


class TestGetOrdersList:

    @title('Проверка на получение списка заказов')
    def test_get_orders(self, orders_api):
        response = orders_api.get_list_orders()
        result = response.json()
        with step('ОР: Код ответа 200'):
            assert response.status_code == 200
        with step('ОР: Тело ответа содержит ключ orders'):
            assert "orders" in result.keys()
        with step('ОР: В теле ответа значение ключа order в виде списка'):
            assert isinstance(result["orders"], list)
