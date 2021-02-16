from Functions import *


toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")



search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "841c0928-c3b4-4576-be5c-c862f6b890ac"

address_ll = toponym_longitude + ',' + toponym_lattitude

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass


json_response = response.json()
lst_of_org = []
for i in range(10):
    try:
        organization = json_response["features"][i]
    except IndexError:
        break
    else:
        org_time = organization["properties"]['CompanyMetaData']['Hours']['Availabilities']
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        delta = "0.005"
        try:
            if org_time[0]['TwentyFourHours']:
                lst_of_org.append((org_point, 'gn'))
        except:
            lst_of_org.append((org_point, 'bl'))
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join(spn_find(toponym)),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": '~'.join(["{0},pm2{1}m".format(org_point[0], org_point[1]) for org_point in lst_of_org])
}


map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
