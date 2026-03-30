from requests import get, post, delete, put

print(put('http://localhost:5000/api/jobs/1').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/jobs/1').json())
print(delete('http://localhost:5000/api/jobs/55').json())

print(get('http://localhost:5000/api/jobs').json())
