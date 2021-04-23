from requests import get, post, put, delete
import pytest

apikey = {'apikey': 'AA61BEF9'}


def test_get_all_users():
    # Вывод всех пользователей
    result = get('http://hamjoshua.pythonanywhere.com/api/users', headers=apikey).json()
    print(result)
    assert isinstance(result['users'], list)


def test_get_one_user():
    # Вывод одного пользователя
    result = get('http://hamjoshua.pythonanywhere.com/api/users/1', headers=apikey).json()
    print(result)
    assert result['users']['id'] == 1


def test_get_wrong_id():
    # Некорректный запрос: пользователя с id = 9999 нет в базе
    result = get('http://hamjoshua.pythonanywhere.com/api/users/9999', headers=apikey).json()
    print(result)
    assert result['message'] == "User 9999 not found"


def test_edit():
    # Изменение пользователя
    result = put('http://hamjoshua.pythonanywhere.com/api/users/2', json=
    {
        'name': 'Test name from API!',
        'email': 'apitest@a',
        'password': 'a',
        'about': 'Test "about" from API!',
        'area': 'USA',
        'role_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_edit_wrong_id():
    # Некорректный запрос: пользователя с id = 9999 нет в базе
    result = put('http://hamjoshua.pythonanywhere.com/api/users/9999', json=
    {
        'name': 'TEST NAME API',
        'email': 'apitest@a',
        'password': 'a',
        'about': 'TEST ABOUT',
        'area': 'USA',
        'role_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['message'] == "User 9999 not found"


def test_edit_not_enough_params():
    # Некорректный запрос: не хватает параметров
    result = put('http://hamjoshua.pythonanywhere.com/api/users/2', json=
    {
        'name': 'TEST NAME API',
        'email': 'apitest@a'
    }, headers=apikey).json()
    print(result)
    assert result['message']['password']


def test_edit_empty_json():
    # Некорректный запрос: пустой json файл
    result = put('http://hamjoshua.pythonanywhere.com/api/users/9999', json={}, headers=apikey).json()
    print(result)
    assert result['message'] == "User 9999 not found"


def test_create():
    # Создание пользователя
    result = post('http://hamjoshua.pythonanywhere.com/api/users', json=
    {
        'name': 'Created name from API!',
        'email': 'create_apitest@a',
        'password': 'a',
        'about': 'Test "about" from API!',
        'area': 'CANADA',
        'role_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_create_not_enough_params():
    # Некорректный запрос: не хватает параметров
    result = post('http://hamjoshua.pythonanywhere.com/api/users', json=
    {
        'name': 'TEST NAME API',
        'email': 'apitest@a'
    }, headers=apikey).json()
    print(result)
    assert result['message']['password']


def test_delete():
    # Получние последнего ID
    max_id = max(get('http://hamjoshua.pythonanywhere.com/api/users', headers=apikey).json()['users'],
                 key=lambda x: x['id'])['id']
    # Удаление пользователя
    result = delete(f'http://hamjoshua.pythonanywhere.com/api/users/{max_id}', headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_delete_wrong_id():
    # Некорректный запрос: пользователя с id = 9999 нет в базе
    result = delete('http://hamjoshua.pythonanywhere.com/api/users/9999', headers=apikey).json()
    print(result)
    assert result['message'] == "User 9999 not found"
