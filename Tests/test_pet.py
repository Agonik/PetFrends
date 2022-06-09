from api import PetFrends
from settings import email, password, password_2
import os

pf = PetFrends()

def test_get_api_key(email=email, password=password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_Invalid_get_api_key(email=email, password=password_2):
    # ввод некорректного пароля
        status, result = pf.get_api_key(email, password)
        assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_create_pet(name='Sem', animal_type='nn', age='2'):
        _, auth_key = pf.get_api_key(email, password)
        status, result = pf.create_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_create_pet_no_data(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_update_pet_info(name='Bob', animal_type='dog', age=11):
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no pets")


def test_create_pet_with_incorrect(name='@@$$', animal_type='!#!',age='&2'):
       # Проверяем, можно ли добавить питомца с некорректными данными
        _, auth_key = pf.get_api_key(email, password)
        status, result = pf.create_pet(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_add_new_pet_no_photo_with_invalid_age(name='Гав', animal_type='кот', age='сказочный'):
    """Проверяем что попытка добавить питомца с неверным возрастом"""

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.create_pet(auth_key, name, animal_type, age)

    assert status == 200




def test_successful_update_self_pet_info(name='Васька', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet(auth_key, "барбос", "пес", "6")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name

        # Удаляем созданную запись
        pet_id = my_pets['pets'][0]['id']
        pf.delete_pet(auth_key, pet_id)
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no pets")

def test_add_new_pet(name='Шарик', animal_type='дворняга', age='7', pet_photo='images/1.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_no_data(name='', animal_type='', age='', pet_photo='images/2.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
