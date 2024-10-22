# weather-predictor

Сервис для предсказания погодных условий по двум точкам маршрута

## Установка на Windows

1. Скачайте репозиторий удобным для вас способом, например, git clone "https://github.com/Zeltq/weather_predictor"
2. Перейдите в каталог проекта в командной строке и введите python -m venv venv
3. Активируйте окружение, введя venv\Scripts\activate
4. Установите необходимые библиотеки, введя pip install -r requirements.txt
5. Создайте файл config.py в основной директории проекта и напишите в нём api_key="YOUR_API_KEY" в кавычках напишите ваш api_key с сайта https://developer.accuweather.com/
5. Запустите файл app.py, введя python app.py
6. Приложение работает, по умолчанию на 5000 порте
