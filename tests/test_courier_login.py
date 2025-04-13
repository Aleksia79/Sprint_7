from allure import title, step

from src.helpers import generate_courier_data


class TestCourierLogin:

    @title('Проверяем, что успешная авторизация курьера возвращает id')
    def test_courier_login_return_id(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step(f'Передаем login:{courier.login} и password:{courier.password} зарегистрированного курьера'):
            courier.login_courier()
        with step('ОР: Код ответа 200'):
            assert courier.response_login.status_code == 200
        with step(f'ОР: id курьера: {courier.response_login.json()['id']}'):
            assert courier.courier_id == courier.response_login.json()["id"]

    @title('Проверяем, что нельзя авторизовать курьера с пустым полем "password"')
    def test_courier_login_empty_password(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step(f'Передаем login: {courier.login} зарегистрированного курьера, в поле password пустое значение'):
            courier.password = ""
            courier.login_courier()
        with step('ОР: Код ответа 400'):
            assert courier.response_login.status_code == 400
        with step('ОР: тело ответа {"message": "Недостаточно данных для входа"}'):
            assert courier.response_login.json() == {"message": "Недостаточно данных для входа"}

    @title('Проверяем, что нельзя авторизовать курьера с пустым полем "login"')
    def test_courier_login_empty_login(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step(f'Передаем password:{courier.password} зарегистрированного курьера, в поле login пустое значение'):
            courier.login = ""
            courier.login_courier()
        with step('ОР: Код ответа 400'):
            assert courier.response_login.status_code == 400
        with step('ОР: тело ответа {"message": "Недостаточно данных для входа"}'):
            assert courier.response_login.json() == {"message": "Недостаточно данных для входа"}

    @title('Проверяем, что нельзя авторизовать курьера под несуществующим пользователем')
    def test_courier_login_non_existent(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step('Генерируем login, password, first_name'):
            courier.login, courier.password, courier.first_name = generate_courier_data()
        with step(f'Передаем сгенерированные login:{courier.login} и password:{courier.password} незарегистрированного '
                  f'курьера'):
            courier.login_courier()
        with step('ОР: Код ответа 400'):
            assert courier.response_login.status_code == 404
        with step('ОР: тело ответа {"message": "Учетная запись не найдена"}'):
            assert courier.response_login.json() == {"message": "Учетная запись не найдена"}

    @title('Проверяем, что нельзя авторизовать курьера без ключа "login"')
    def test_courier_login_no_key_login(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step(f'Передаем password:{courier.password} зарегистрированного курьера без ключа login'):
            courier.courier_login_data = {"password": courier.password}
        courier.login_courier()
        with step('ОР: Код ответа 400'):
            assert courier.response_login.status_code == 400
        with step('ОР: тело ответа {"message": "Недостаточно данных для входа"}'):
            assert courier.response_login.json() == {"message": "Недостаточно данных для входа"}

    @title('Проверяем, что нельзя авторизовать курьера без ключа "password"')
    def test_courier_login_no_key_password(self, create_courier_and_return_object):
        courier = create_courier_and_return_object
        with step(f'Передаем login:{courier.login} зарегистрированного курьера без ключа password'):
            courier.courier_login_data = {"login": courier.login}
        courier.login_courier()
        with step('ОР: Код ответа 400'):
            assert courier.response_login.status_code == 400
        with step('ОР: тело ответа {"message": "Недостаточно данных для входа"}'):
            assert courier.response_login.json() == {"message": "Недостаточно данных для входа"}
