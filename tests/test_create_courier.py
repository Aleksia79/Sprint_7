from allure import title, step
from src.helpers import generate_courier_data


class TestCreateCourier:

    @title('Проверяем, что успешная регистрация курьера возвращает правильные код и тело ответа')
    def test_create_courier(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step('ОР: запрос возвращает код ответа 201'):
            assert courier.response_create.status_code == 201
        with step('ОР: в теле ответа на запрос получаем {"ok": True}'):
            assert courier.response_create.json() == {"ok": True}

    @title('Проверяем, что нельзя создать двух одинаковых курьеров')
    def test_cant_create_courier_repeat(self, create_courier_and_return_object, courier_api):
        courier_1 = create_courier_and_return_object
        with (step('Повторно передаем сгенерированные login, password, first_name курьера')):
            courier_2 = courier_api
            courier_2.create_courier(courier_1.login, courier_1.password, courier_1.first_name)
        with step('ОР: запрос возвращает код ответа 409'):
            assert courier_2.response_create.status_code == 409
        with step('ОР: в теле ответа на запрос получаем {"message": "Этот логин уже используется"}'):
            assert courier_2.response_create.json() == {"message": "Этот логин уже используется"}

    @title('Проверяем, что нельзя создать курьера с пустым полем "login"')
    def test_cant_create_courier_empty_login(self, courier_api):
        with step('Генерируем login, password, first_name курьера'):
            login, password, first_name = generate_courier_data()
        with step('Отправляем сгенерированные password, first_name курьера, параметр login передаем с пустым '
                  'значением '):
            courier = courier_api
            courier.create_courier("", password, first_name)
        with step('ОР: запрос возвращает код ответа 400'):
            assert courier.response_create.status_code == 400
        with step('ОР: в теле ответа на запрос получаем {"message": "Недостаточно данных для создания учетной '
                  'записи"}'):
            assert courier.response_create.json() == {"message": "Недостаточно данных для создания учетной записи"}

    @title('Проверяем, что нельзя создать курьера с пустым полем "password"')
    def test_cant_create_courier_empty_password(self, courier_api):
        with step('Генерируем login, password, first_name курьера'):
            login, password, first_name = generate_courier_data()
        with step('Отправляем сгенерированные login, first_name курьера, параметр password передаем с пустым '
                  'значением '):
            courier = courier_api
            courier.create_courier(login, "", first_name)
        with step('ОР: запрос возвращает код ответа 400'):
            assert courier.response_create.status_code == 400
        with step('ОР: в теле ответа на запрос получаем {"message": "Недостаточно данных для создания учетной '
                  'записи"}'):
            assert courier.response_create.json() == {"message": "Недостаточно данных для создания учетной записи"}

    @title('Проверяем, что нельзя создать курьера с пустым полем "firstName"')
    def test_cant_create_courier_empty_first_name(self, courier_api):
        with step('Генерируем login, password, first_name курьера'):
            login, password, first_name = generate_courier_data()
        with step('Отправляем сгенерированные login, password курьера, параметр firstName передаем с пустым '
                  'значением '):
            courier = courier_api
            courier.create_courier(login, password, "")
        with step('ОР: запрос возвращает код ответа 400'):
            assert courier.response_create.status_code == 400
        with step('ОР: в теле ответа на запрос получаем {"message": "Недостаточно данных для создания учетной '
                  'записи"}'):
            assert courier.response_create.json() == {"message": "Недостаточно данных для создания учетной записи"}
