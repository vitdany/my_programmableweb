import json
#Что находиться рядом по гео координатам
import requests
from pprint import pprint
main_link = 'http://api.geonames.org/findNearbyJSON'
params = {'username':'danilenkovv',
          'lat':'47.3',
          'lng':'9'
            }

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
           'Accept':'*/*'}

response = requests.get(main_link, params=params, headers=headers)
j_body = response.json()

pprint(f"Страна {j_body['geonames'][0]['countryName']}")
pprint(f"Административный центр {j_body['geonames'][0]['adminName1']}")
pprint(f"Место {j_body['geonames'][0]['toponymName']}")


with open('response_geonames.json', 'w') as f:
    json.dump(j_body, f)