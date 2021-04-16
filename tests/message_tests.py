from requests import get, post, put, delete

# Вывод всех комментариев
print(get('http://localhost:8000/api/messages').json())

# Вывод одного комментария
print(get('http://localhost:8000/api/messages/1').json())

# Некорректный запрос: комментария с id = 9999 нет в базе
print(get('http://localhost:8000/api/messages/9999').json())

# Изменение комментария
print(put('http://localhost:8000/api/messages/2', json=
          {
              'message': 'TEST MESSAGE',
              'topic_id': 1,
              'author_id': 1
          }).json()
      )

# Некорректный запрос: комментария с id = 9999 нет в базе
print(put('http://localhost:8000/api/messages/9999', json=
          {
              'message': 'TEST MESSAGE',
              'topic_id': 1,
              'author_id': 1
          }).json()
      )

# Некорректный запрос: не хватает параметров
print(put('http://localhost:8000/api/messages/2', json=
          {
              'message': 'TEST MESSAGE',
              'author_id': 1
          }).json()
      )

# Некорректный запрос: пустой json файл
print(put('http://localhost:8000/api/messages/9999', json={}).json())

# Создание комментария
print(post('http://localhost:8000/api/messages', json=
           {
              'message': 'TEST message CREATED MESSAGE',
              'topic_id': 1,
              'author_id': 1
           }).json()
      )


# Некорректный запрос: author_id не число
print(post('http://localhost:8000/api/messages', json=
           {
              'message': 'TEST message CREATED MESSAGE',
              'topic_id': 1,
              'author_id': 'ddd'
           }).json()
      )

# Некорректный запрос: не хватает параметров
print(post('http://localhost:8080/api/messages', json=
           {
               'title': 'TEST TITLE CREATED MESSAGE'
           }).json()
      )

# Удаление комментария
print(delete('http://localhost:8080/api/messages/2').json())

# Некорректный запрос: комментария с id = 9999 нет в базе
print(delete('http://localhost:8080/api/messages/9999').json())
