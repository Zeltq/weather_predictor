'''
Файл для задания 1. 
Реализованы функции для:
получения ключа по названию города;
получение ключа по широте и долготе
Получения текущей погоды;
Получение прогноза погоды на день вперёд;
'''


import requests
import json
from config import api_key


def get_location_key_by_city(city: str, api_key: str) -> str:
    '''
    Эта функцию принимает название города и возвращает его location_key
    '''
    location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}"
    location_response = requests.get(location_url)

    if location_response.status_code != 200:
        raise Exception(f"Ошибка при получении ключа местоположения: {location_response.json()}")

    location_data = location_response.json()
    if not location_data:
        raise Exception(f"Город '{city}' не найден")

    location_key = location_data[0]['Key']
    return str(location_key)

def get_location_key_by_lat_lon(lat: str, lon: str,  api_key: str) -> str:
    '''
    Эта функцию для первого задания принимает широту и долготу, 
    а возвращает location_key по этим данным
    '''
    location_url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={lat}%2C{lon}&details=true"
    location_response = requests.get(location_url)

    if location_response.status_code != 200:
        raise Exception(f"Ошибка при получении ключа местоположения: {location_response.json()}")

    location_data = location_response.json()
    if not location_data:
        raise Exception("Ошибка в get_location_key_by_lat_lon")

    location_key = location_data['Key']
    return str(location_key)

def get_current_weather(location_key: str, api_key: str) -> str:
    '''
    Это функция для первого задания с текущим состоянием погоды и соответственными данными.
    Для основной работы приложения будем использоваться следующую функцию (get_daily_forecast)
    
    '''

    # Получаем данные о погоде по ключу местоположения
    weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}&details=true"
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        raise Exception(f"Ошибка при получении данных о погоде: {weather_response.json()}")

    weather_data = weather_response.json() # Преобразуем в json для удобной дальнейшей работы

    # Извлекаем нужные параметры
    temperature = weather_data[0]['Temperature']['Metric']['Value']
    humidity = weather_data[0]['RelativeHumidity']
    wind_speed = weather_data[0]['Wind']['Speed']['Metric']['Value']
    pressure = weather_data[0]['Pressure']['Metric']['Value']

    # Формируем словарь с результатами
    result = {
        'Температура (°C)': temperature,
        'Влажность (%)': humidity,
        'Скорость ветра (м/с)': wind_speed,
        'Давление (милибары)': pressure,

    }

    return json.dumps(result, ensure_ascii=False)

def get_daily_forecast(location_key: str, api_key: str) -> str:
    '''
    Эта функция по ключу локации достаёт основные данные о погоде.
    '''
    # Получаем данные о погоде на день по ключу местоположения
    weather_url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&details=true&metric=true"
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        raise Exception(f"Ошибка при получении данных о погоде: {weather_response.json()}")

    weather_data = weather_response.json() # Преобразуем в json для удобной дальнейшей работы

    # Извлекаем нужные параметры
    max_temperature = weather_data['DailyForecasts'][0]['Temperature']['Maximum']['Value']
    min_temperature = weather_data['DailyForecasts'][0]['Temperature']['Minimum']['Value']
    precipitation_probability = weather_data['DailyForecasts'][0]['Day']['PrecipitationProbability']
    wind_speed = weather_data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']


    # Формируем словарь с результатами
    result = {
        'Максимальная температура (°C)': max_temperature,
        'Минимальная температура (°C)': min_temperature,
        'Вероятность осадков (%)': precipitation_probability,
        'Скорость ветра (км/ч)': wind_speed,
    }

    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    try:
        location_key = get_location_key_by_lat_lon(lat=55.77, lon=37.607, api_key=api_key) #Координаты Москвы
        weather_info_current = get_current_weather(location_key, api_key)
        #weather_info_forecast = get_daily_forecast(location_key, api_key)
        #print(weather_info_forecast)
        print(location_key)
        print(weather_info_current)
    except Exception as e:
        print('ERROR', e)

