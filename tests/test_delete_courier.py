from allure import title, step


class TestDeleteCourier:

    @title('Проверка удаления курьера по его id')
    def test_delete_courier(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step('Передаем корректный id курьера'):
            response = courier.delete_courier_by_id(courier.courier_id)
        with step('ОР: Код ответа: 200'):
            assert response.status_code == 200
        with step('ОР: В теле ответа на запрос получаем {"ok": True}'):
            assert response.json() == {"ok": True}

    @title('Проверка удаления курьера при запросе без id')
    def test_delete_courier_no_id(self, courier_api):
        with step('Отправляем запрос без id курьера'):
            response = courier_api.delete_courier_by_id("")
        with step('ОР: Код ответа 400'):
            assert response.status_code == 400
        with step('ОР: В теле ответа на запрос получаем {"Недостаточно данных для удаления курьера"}'):
            assert response.json() == {"message": "Недостаточно данных для удаления курьера"}

    @title('Проверка удаления курьера с несуществующим id')
    def test_delete_courier_non_existent_id(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        courier_id = courier.courier_id
        with step('Отправляем запрос на удаление курьера с существующим id'):
            courier.delete_courier_by_id(courier.courier_id)
        with step('Отправляем запрос на удаление удаленного курьера'):
            response = courier.delete_courier_by_id(courier_id)
        with step('ОР: Код ответа 404'):
            assert response.status_code == 404
        with step('ОР: В теле ответа на запрос получаем {"Курьера с таким id нет"}'):
            assert response.json() == {"message": "Курьера с таким id нет"}


