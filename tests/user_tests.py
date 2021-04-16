from requests import get, post, put, delete

# Вывод всех пользователей
print(get('http://localhost:8000/api/users').json())

# Вывод одного пользователя
print(get('http://localhost:8000/api/users/1').json())

# Некорректный запрос: пользователя с id = 9999 нет в базе
print(get('http://localhost:8000/api/users/9999').json())

# Изменение пользователя
print(put('http://localhost:8000/api/users/2', json=
          {
              'name': 'TEST NAME API',
              'email': 'apitest@a',
              'password': 'a',
              'about': 'TEST ABOUT',
              'area': 'USA',
              'role_id': 1
          }).json()
      )

# Некорректный запрос: пользователя с id = 9999 нет в базе
print(put('http://localhost:8000/api/users/9999', json=
          {
              'name': 'TEST NAME API',
              'email': 'apitest@a',
              'password': 'a',
              'about': 'TEST ABOUT',
              'area': 'USA',
              'role_id': 1
          }).json()
      )

# Некорректный запрос: не хватает параметров
print(put('http://localhost:8000/api/users/2', json=
          {
              'name': 'TEST NAME API',
              'email': 'apitest@a'
          }).json()
      )

# Некорректный запрос: пустой json файл
print(put('http://localhost:8000/api/users/9999', json={}).json())

# Создание пользователя
print(post('http://localhost:8000/api/users', json=
           {
              'name': 'TEST NAME API',
              'email': 'apitest@a',
              'password': 'a',
              'about': 'TEST ABOUT',
              'area': 'USA',
              'role_id': 1
           }).json()
      )


# Некорректный запрос: role_id не число
print(post('http://localhost:8000/api/users', json=
           {
              'name': 'TEST NAME API',
              'email': 'apitest@a',
              'password': 'a',
              'about': 'TEST ABOUT',
              'area': 'USA',
              'role_id': 's'
           }).json()
      )

# Некорректный запрос: не хватает параметров
print(post('http://localhost:8080/api/users', json=
           {
               'name': 'TEST NAME API',
               'email': 'apitest@a'
           }).json()
      )

# Удаление пользователя
print(delete('http://localhost:8080/api/users/2').json())

# Некорректный запрос: пользователя с id = 9999 нет в базе
print(delete('http://localhost:8080/api/users/9999').json())
