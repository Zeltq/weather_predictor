'''
Файл основы Flask приложения. Обрабатывает методы GET и POST к сервису
'''

from flask import Flask, render_template, request
import json

from config import api_key
from estimation import get_weather_is_bad
from functs import get_daily_forecast, get_location_key_by_city


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_city = request.form['start_city']
        
        end_city = request.form['end_city']
        print(start_city, end_city)

        try:
            # Получаем location_key для каждого города
            start_location_key = get_location_key_by_city(start_city, api_key)
            end_location_key = get_location_key_by_city(end_city, api_key)
            print(start_location_key, end_location_key)

            # Получаем прогноз погоды для каждого города
            start_weather = json.loads(get_daily_forecast(start_location_key, api_key))
            end_weather = json.loads(get_daily_forecast(end_location_key, api_key))
            print(start_weather)
            print(end_weather)

            # Проверяем, является ли погода хорошей или плохой
            start_weather_good = get_weather_is_bad(start_weather)
            end_weather_good = get_weather_is_bad(end_weather)
            print(start_weather_good)

            # Формируем сообщения для отображения пользователю
            start_message = "Ой-ой, погода плохая" if start_weather_good else "Погода супер"
            end_message = "Ой-ой, погода плохая" if end_weather_good else "Погода супер"

            # Рендерим страницу с соответствующими данными
            return render_template('index.html', start_message=start_message, end_message=end_message)
        
        # Обработка ошибок. Стоит отметить, что в функциях из файла functs.py большинство ошибок уже обработаны.
        except json.JSONDecodeError:  # Обработка ошибок декодирования JSON
            return render_template('index.html', error="Ошибка обработки данных о погоде.")
        
        except Exception as e:  # Общая обработка ошибок
            return render_template('index.html', error=f"Ошибка: {e}. Данные недоступны")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False)
