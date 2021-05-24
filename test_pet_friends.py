from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


# ПОЗИТИВНЫЕ ТЕСТЫ

def test_add_new_pet_without_photo_with_valid_data(name='страус', animal_type='рил', age='6'):
    """Проверяем, что можно добавить питомца с корректными данными, но без фото"""
    # Получаем ключ auth_key и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца(без фото)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_get_api_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Далее, используя этого ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Используя ключ auth_key, запрашиваем список всех питомцев и проверяем,
    # что список не пустой. Доступное значение параметра filter - 'my_pets', либо ''
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='пес', animal_type='обычный',
                                     age='3', pet_photo='images/pesel.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Саня", "пёс", "2", "images/zayats.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet_info(name="Коте", animal_type="огромный", age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('There is not my pets')


def test_successful_add_photo_of_pet_with_valid_data(pet_photo='images/pesel.jpg'):
    """Проверяем, что можно добавить фото питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "ня", "kec", "8")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] is not ''


# НЕГАТИВНЫЕ ТЕСТЫ

def test_invalid_get_for_password(email="kirill_srpti@mail.ru", password="12345"):
    """Негативный тест на ввод неправильного пароля для аутентификации"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "<title>403 Forbidden</title>" in result
    assert "<p>This user wasn't found in database</p>" in result


def test_invalid_get_for_login(email="dfgereg", password="kirill99"):
    """Негативный тест на неправильный ввод логина для аутентификации"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "<title>403 Forbidden</title>" in result
    assert "<p>This user wasn't found in database</p>" in result


def test_get_list_of_pets_with_invalid_auth_key(filter=''):
    """Негативный тест на получение списка питомцев при использовании НЕВЕРНОГО
     ключа API, который используется для аутентификации  """

    # Добавляем неверный API ключ аутентификации
    auth_key = {'key': 'skfl43hl34h53454df6g434v5'}
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "<title>403 Forbidden</title>" in result
    assert "<p>Please provide 'auth_key' Header</p>" in result


def test_get_list_of_pets_with_invalid_empty_auth_key(filter=''):
    """Негативный тест на получение списка питомцев при использовании ПУСТОГО
     ключа API, который используется для аутентификации  """

    # Добавляем неверный(пустой) API ключ аутентификации
    auth_key = {'key': ''}

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert "<title>403 Forbidden</title>" in result
    assert "<p>Please provide 'auth_key' Header</p>" in result


def test_add_new_pet_with_valid_data_but_with_emply_auth_key(name='пес', animal_type='обычный',
                                                      age='3', pet_photo='images/pesel.jpg'):
    """Негативный тест на добавление питомца с пустым ключом API"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем пустой API ключ аутентификации
    auth_key = {'key': ''}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert "<title>403 Forbidden</title>" in result
    assert "<p>Please provide 'auth_key' Header</p>" in result


def test_add_new_pet_with_valid_data_but_with_invalid_auth_key(name='пес', animal_type='обычный',
                                                               age='3', pet_photo='images/pesel.jpg'):
    """Негативный тест на добавление питомца с неверным ключом API"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем неверный API ключ аутентификации
    auth_key = {'key': 'dfulhgdkfg3458348597'}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert "<title>403 Forbidden</title>" in result
    assert "<p>Please provide 'auth_key' Header</p>" in result


def test_add_new_pet_without_photo_with_invalid_data(name='', animal_type='',
                                                     age=''):
    """Негативный тест на добавление питомца с пустыми данными без фото"""

    # Получаем ключ auth_key и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца(без фото)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_add_new_pet_without_photo_with_negative_age(name='гусь', animal_type='обычный',
                                                     age='-4'):
    """Негативный тест на добавление питомца с отрицательным возрастом без фото"""

    # Получаем ключ auth_key и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца(без фото)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


def test_delete_pet_with_invalid_auth_key():
    """Негативный тест для проверки возможности удаления существующего
     питомца с помощью неверного API ключа"""

    # Используем API ключ для получения существующего id питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    if len(list_of_pets['pets']) > 0:
        pet_id = list_of_pets['pets'][0]['id']

        # Меняем ключ на несуществующий и пытаемся удалить питомца
        auth_key = {'key': 'dkfgbdufb93459384'}
        status, _ = pf.delete_pet(auth_key, pet_id)
        assert status == 403
    else:
        raise Exception("Список питомцев пуст")


def test_delete_pet_of_another_user_with_valid_key():
    """Негативный тест для проверки возможности удаления существующего
    питомца с помощью API ключа другого пользователя"""

    # Получаем наш API ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Используем пустой фильтр для получения списка питомцев всех пользователей
    _, list_of_pets = pf.get_list_of_pets(auth_key, '')

    if len(list_of_pets['pets']) > 0:

        # Берем id питомца, которое не принадлежит владельцу ключа
        pet_id = list_of_pets['pets'][25]['id']

        # Пытаемся удалить питомца с этим id
        status, _ = pf.delete_pet(auth_key, pet_id)
        assert status == 403
    else:
        raise Exception('Список питомцев пуст')


def test_add_photo_of_pet_of_another_user(pet_photo='images/pesel.jpg'):
    """Негативный тест для проверки возможности изменения фото чужого питомца с
    помощью своего API ключа"""

    # Получаем свой API ключ и список всех питомцев на сайте
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, list_of_pets = pf.get_list_of_pets(auth_key, '')

    # Выбираем любого питомца и пытаемся ему поменять фото
    pet_id = list_of_pets['pets'][20]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 400


def test_add_new_pet_with_text_as_photo_impossible(name='пес', animal_type='обычный', age='5',
                                                   pet_photo='images/yes_eto_text.txt'):
    """Негативный тест для проверки возможности загрузки текстового документа вместо фото"""

    # Получаем свой API ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пытаемся загрузить текстовый документ вместо изображения
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400







