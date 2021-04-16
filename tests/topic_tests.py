from requests import get, post, put, delete

# Вывод всех тем
print(get('http://localhost:8000/api/topics').json())

# Вывод одной темы
print(get('http://localhost:8000/api/topics/1').json())

# Некорректный запрос: темы с id = 9999 нет в базе
print(get('http://localhost:8000/api/topics/9999').json())

# Изменение темы
print(put('http://localhost:8000/api/topics/2', json=
          {
              'title': 'TEST TITLE TOPIC',
              'text': 'TEST TEXT TOPIC',
              'category_id': 1,
              'author_id': 1
          }).json()
      )

# Некорректный запрос: темы с id = 9999 нет в базе
print(put('http://localhost:8000/api/topics/9999', json=
          {
              'title': 'TEST TITLE TOPIC',
              'text': 'TEST TEXT TOPIC',
              'category_id': 1,
              'author_id': 1
          }).json()
      )

# Некорректный запрос: не хватает параметров
print(put('http://localhost:8000/api/topics/2', json=
          {
              'title': 'TEST TITLE TOPIC',
              'text': 'TEST TEXT TOPIC',
              'author_id': 1
          }).json()
      )

# Некорректный запрос: пустой json файл
print(put('http://localhost:8000/api/topics/9999', json={}).json())

# Создание темы
print(post('http://localhost:8000/api/topics', json=
           {
              'title': 'TEST TITLE CREATED TOPIC',
              'text': 'TEST TEXT CREATED TOPIC',
              'category_id': 1,
              'author_id': 1
           }).json()
      )


# Некорректный запрос: author_id не число
print(post('http://localhost:8000/api/topics', json=
           {
              'title': 'TEST TITLE CREATED TOPIC',
              'text': 'TEST TEXT CREATED TOPIC',
              'category_id': 1,
              'author_id': 'ddd'
           }).json()
      )

# Некорректный запрос: не хватает параметров
print(post('http://localhost:8080/api/topics', json=
           {
               'title': 'TEST TITLE CREATED TOPIC'
           }).json()
      )

# Удаление темы
print(delete('http://localhost:8080/api/topics/2').json())

# Некорректный запрос: темы с id = 9999 нет в базе
print(delete('http://localhost:8080/api/topics/9999').json())
