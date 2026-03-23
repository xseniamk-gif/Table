from requests import get, post

# print(get('http://localhost:5000/api/jobs').json())
# print(get('http://localhost:5000/api/jobs/1').json())
#
# print(get('http://localhost:5000/api/jobs/999').json())
# print(get('http://localhost:5000/api/jobs/q').json())
# print(post('http://localhost:5000/api/news', json={}).json())
#
# print(post('http://localhost:5000/api/news',
#            json={'title': 'Заголовок'}).json())

print(post('http://localhost:5000/api/news',
           # 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished',
           #                   'user.name'
           json={'team_leader': 33,
                 'job': 'Cool work with API',
                 'work_size': 13,
                 'collaborators': '1,2',
                 'is_finished': False}).json())