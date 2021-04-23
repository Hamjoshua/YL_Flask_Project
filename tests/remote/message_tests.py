from requests import get, post, put, delete
import pytest

apikey = {'apikey': 'AA61BEF9'}


def test_get_all_comments():
    # Вывод всех комментариев
    result = get('http://hamjoshua.pythonanywhere.com/api/messages', headers=apikey).json()
    print(result)
    assert isinstance(result['message'], list)


def test_get_comment():
    # Вывод одного комментария
    result = get('http://hamjoshua.pythonanywhere.com/api/messages/1', headers=apikey).json()
    print(result)
    assert result['message']['id'] == 1


def test_get_wrong_id():
    # Некорректный запрос: комментария с id = 9999 нет в базе
    result = get('http://hamjoshua.pythonanywhere.com/api/messages/9999', headers=apikey).json()
    print(result)
    assert result['message'] == 'Message 9999 not found'


def test_edit():
    # Изменение комментария
    result = put('http://hamjoshua.pythonanywhere.com/api/messages/2', json=
    {
        'message': 'Message edited from API!',
        'topic_id': 1,
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_edit_wrong_id():
    # Некорректный запрос: комментария с id = 9999 нет в базе
    result = put('http://hamjoshua.pythonanywhere.com/api/messages/9999', json=
    {
        'message': 'TEST MESSAGE',
        'topic_id': 1,
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['message'] == 'Message 9999 not found'


def test_edit_not_enough_params():
    # Некорректный запрос: не хватает параметров
    result = put('http://hamjoshua.pythonanywhere.com/api/messages/2', json=
    {
        'message': 'TEST MESSAGE',
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['message']['topic_id']


def test_edit_empty_json():
    # Некорректный запрос: пустой json файл
    result = put('http://hamjoshua.pythonanywhere.com/api/messages/9999', json={}, headers=apikey).json()
    print(result)
    assert result['message'] == 'Message 9999 not found'


def test_create():
    # Создание комментария
    result = post('http://hamjoshua.pythonanywhere.com/api/messages', json=
    {
        'message': 'TEST message CREATED MESSAGE',
        'topic_id': 1,
        'author_id': 1
    }, headers=apikey).json()
    print(result)
    assert result['success']


def test_create_not_enough_params():
    # Некорректный запрос: не хватает параметров
    result = post('http://hamjoshua.pythonanywhere.com/api/messages', json=
    {
        'title': 'TEST TITLE CREATED MESSAGE'
    }, headers=apikey).json()
    print(result)
    assert not result.get('message', None) is None


def test_delete():
    # Получение ID последнего сообщения
    max_id = max(get('http://hamjoshua.pythonanywhere.com/api/messages', headers=apikey).json()['message'],
                 key=lambda x: x['id'])['id']
    # Удаление комментария
    result = delete(f'http://hamjoshua.pythonanywhere.com/api/messages/{max_id}', headers=apikey).json()
    print(result)
    assert result['success'] == 'OK'


def test_delete_wrong_id():
    # Некорректный запрос: комментария с id = 9999 нет в базе
    result = delete('http://hamjoshua.pythonanywhere.com/api/messages/9999', headers=apikey).json()
    print(result)
    assert result['message'] == 'Message 9999 not found'
