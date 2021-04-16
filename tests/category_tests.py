from requests import get, post, put, delete

# Вывод всех тем
print(get('http://localhost:8000/api/categories').json())

# Вывод одной категории
print(get('http://localhost:8000/api/categories/1').json())

# Некорректный запрос: категории с id = 9999 нет в базе
print(get('http://localhost:8000/api/categories/9999').json())

# Изменение категории
print(put('http://localhost:8000/api/categories/2', json=
          {
              'title': 'TEST TITLE CATEGORY'
          }).json()
      )

# Некорректный запрос: категории с id = 9999 нет в базе
print(put('http://localhost:8000/api/categories/9999', json=
          {
              'title': 'TEST TITLE CATEGORY'
          }).json()
      )

# Некорректный запрос: пустой json файл
print(put('http://localhost:8000/api/categories/9999', json={}).json())

# Создание категории
print(post('http://localhost:8000/api/categories', json=
           {
              'title': 'TEST TITLE CREATED CATEGORY'
           }).json()
      )

# Некорректный запрос: не хватает параметров
print(post('http://localhost:8080/api/categories', json={}).json())

# Удаление категории
print(delete('http://localhost:8080/api/categories/2').json())

# Некорректный запрос: категории с id = 9999 нет в базе
print(delete('http://localhost:8080/api/categories/9999').json())
