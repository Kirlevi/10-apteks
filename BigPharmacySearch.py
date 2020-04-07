import sys
import math
from io import BytesIO
import requests
from PIL import Image
import GeocoderParams
import OrgSearch

# program1.py Москва, ул. Ак. Королева, 12

toponym_to_find = " ".join(sys.argv[1:])

toponym = GeocoderParams.address_to_geocode(toponym_to_find)

lat, lon = GeocoderParams.get_coordinates(toponym_to_find)
coord = f'{lat},{lon}'
span = '0.015,0.015'

org = OrgSearch.find_businesses(coord, span, 'аптека')

# для метки на карте и подсчета расстояния
org_lat, org_lon = org[0]['geometry']['coordinates']

pt = ",".join([str(lat), str(lon), 'org']) + '~'
for i in range(10):
    org_lat, org_lon = org[i]['geometry']['coordinates']
    print(org_lat, org_lon)
    try:
        if org[i]['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['TwentyFourHours']:
            pt += ",".join([str(org_lat), str(org_lon), 'pmgnm'])
        elif org[i]['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['Intervals'][0]['from']:
            pt += ",".join([str(org_lat), str(org_lon), 'pmblm'])
    except Exception:
        pt += ",".join([str(org_lat), str(org_lon), 'pmgrm'])
    pt += '~'
pt = pt[:-1]


map_params = {
    "ll": ",".join([str(lat), str(lon)]),
    "pt": pt,
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()