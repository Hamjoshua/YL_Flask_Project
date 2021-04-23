from requests import get, post, put, delete
import pytest

apikey = {'apikey': 'AA61BEF9'}


def test_get_all_tests():
    # Вывод всех тем
    assert isinstance(
        get('http://localhost:8080/api/categories', headers=apikey).json()['categories'], list)


def test_apikey_not_found():
    # Неккоректный запрос: ключ API отсутствует
    assert get('http://localhost:8080/api/categories').json()['message'] == 'Invalid API-key'


def test_wrong_apikey():
    # Неккоректный запрос: неверный ключ API
    assert get('http://localhost:8080/api/categories', headers={'apikey': 'not_exist'}).json()[
               'message'] == 'Invalid API-key'


def test_get_one_category():
    # Вывод одной категории
    assert get('http://localhost:8080/api/categories/1', headers=apikey).json()['categories'][
               'id'] == 1


def test_get_wrong_id_category():
    # Некорректный запрос: категории с id = 9999 нет в базе
    assert get('http://localhost:8080/api/categories/9999', headers=apikey).json()[
               'message'] == 'Category 9999 not found'


def test_edit_category():
    # Изменение категории
    assert put('http://localhost:8080/api/categories/2', json={
        'title': 'Edited title from API!'
    }, headers=apikey).json()['success'] == 'OK'


def test_edit_wrong_id_category():
    # Некорректный запрос: категории с id = 9999 нет в базе
    assert put('http://localhost:8080/api/categories/9999', json={
        'title': 'TEST TITLE CATEGORY'
    }, headers=apikey).json()['message'] == 'Category 9999 not found'


def test_edit_empty_json():
    result = put('http://localhost:8080/api/categories/9999', json={}, headers=apikey).json()
    print(result)
    # Некорректный запрос: пустой json файл
    assert result['message'] == 'Category 9999 not found'


def test_create_category():
    result = post('http://localhost:8080/api/categories', json={
        'title': 'Test category from API!'}, headers=apikey).json()
    # Создание категории
    assert result['success'] == 'OK'


def test_create_empty_json():
    # Некорректный запрос: пустой json файл
    assert not post('http://localhost:8080/api/categories', json={}, headers=apikey).json().get(
        'message', None) is None


def test_delete_category():
    # Удаление категории
    assert delete(f'http://localhost:8080/api/categories/32', headers=apikey).json()[
               'success'] == 'OK'


def test_delete_wrong_category_id():
    # Некорректный запрос: категории с id = 9999 нет в базе
    assert delete('http://localhost:8080/api/categories/9999', headers=apikey).json()[
               'message'] == 'Category 9999 not found'
