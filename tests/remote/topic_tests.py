from requests import get, post, put, delete
import pytest

apikey = {'apikey': 'AA61BEF9'}


def test_get_all_topics():
    # Вывод всех тем
    result = get('http://hamjoshua.pythonanywhere.com/api/topics', headers=apikey).json()
    print(result)
    assert isinstance(result['topics'], list)


def test_get_one_topic():
    # Вывод одной темы
    result = get('http://hamjoshua.pythonanywhere.com/api/topics/1', headers=apikey).json()
    print(result)
    assert result['topics']['id'] == 1


def test_get_wrong_id():
    # Некорректный запрос: темы с id = 9999 нет в базе
    result = get('http://hamjoshua.pythonanywhere.com/api/topics/9999', headers=apikey).json()
    print(result)
    assert result['message'] == 'Topic 9999 not found'


def test_edit():
    # Изменение темы
    result = put('http://hamjoshua.pythonanywhere.com/api/topics/2', json=
    {
        'title': 'Edited title from API!',
        'text': 'Edited text from API!',
        'category_id': 1,
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_edit_wrong_id():
    # Некорректный запрос: темы с id = 9999 нет в базе
    result = put('http://hamjoshua.pythonanywhere.com/api/topics/9999', json=
    {
        'title': 'Edited title from API!',
        'text': 'Edited text from API!',
        'category_id': 1,
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['message'] == 'Topic 9999 not found'


def test_edit_not_enough_params():
    # Некорректный запрос: не хватает параметров
    result = put('http://hamjoshua.pythonanywhere.com/api/topics/2', json=
    {
        'title': 'TEST TITLE TOPIC',
        'text': 'TEST TEXT TOPIC',
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['message']['category_id']


def test_edit_empty_json():
    # Некорректный запрос: пустой json файл
    result = put('http://hamjoshua.pythonanywhere.com/api/topics/9999', json={}, headers=apikey).json()
    assert result['message'] == 'Topic 9999 not found'


def test_create():
    # Создание темы
    result = post('http://hamjoshua.pythonanywhere.com/api/topics', json=
    {
        'title': 'TEST TITLE CREATED TOPIC',
        'text': 'TEST TEXT CREATED TOPIC',
        'category_id': 1,
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_create_not_enough_params():
    # Некорректный запрос: не хватает параметров
    result = post('http://hamjoshua.pythonanywhere.com/api/topics', json=
    {
        'title': 'TEST TITLE CREATED TOPIC'
    }, headers=apikey).json()
    print(result)
    assert result['message']['text']


def test_delete():
    # Получение последнего ID
    max_id = max(get('http://hamjoshua.pythonanywhere.com/api/topics', headers=apikey).json()['topics'], key=lambda x: x['id'])[
        'id']
    # Удаление темы
    result = delete(f'http://hamjoshua.pythonanywhere.com/api/topics/{max_id}', headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_delete_wrong_id():
    # Некорректный запрос: темы с id = 9999 нет в базе
    result = delete('http://hamjoshua.pythonanywhere.com/api/topics/9999', headers=apikey).json()
    print(result)
    assert result['message'] == 'Topic 9999 not found'
