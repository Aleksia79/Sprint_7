import random
import string


# метод генерирует строку, состоящую только из букв нижнего регистра
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


# метод генерирует login, password и first_name для создания курьера
def generate_courier_data(login=None, password=None, first_name=None):
    if login is None:
        login = generate_random_string(10)
    if password is None:
        password = generate_random_string(10)
    if first_name is None:
        first_name = generate_random_string(10)
    return login, password, first_name


