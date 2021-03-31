import json
import requests
from pprint import pprint
main_link = 'https://api.github.com/users/vitdany/repos'
response = requests.get(main_link)

j_body = response.json()
print(f'status= { response.status_code}')

for i in j_body:
    print(i['name'])

with open('response_github.json', 'w') as f:
    json.dump(j_body, f)