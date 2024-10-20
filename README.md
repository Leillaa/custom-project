# bbt_backend
Проект телеграм бота для Большой Байкальской Тропы

# База данных
Структура Базы Данных внесена в Miro доску проекта (локация слева)
Ссылка: https://miro.com/welcomeonboard/amRnWnJBN3hjWGZ0N254M1A5NXFQc1Frd3l6cW5KMHkxUEp3MEUzNjRtdE52OGtNVTdHUFlEeERubjZqVE11MHwzMDc0NDU3MzY0OTM3ODY2MDE3?invite_link_id=806747411105

### Этапы запуска приложения на локальной машине:
1. Установите <a href=https://docs.docker.com/engine/install/ubuntu/>docker</a>
2. Клонируйте проект в рабочую директорию:<br> 
```git clone https://github.com/Studio-Yandex-Practicum/bbt_backend.git```
3. Создайте файл .env (в директории bbt_backend/bbt_admin/bbt_admin рядом с settings.py) с переменными окружения:<br> 
SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT<br>
4. Сборка и запуск контейнеров:<br>
```docker-compose -f docker-compose.local.yml up -d```<br>
