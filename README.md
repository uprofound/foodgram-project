[![foodgram_workflow](https://github.com/uprofound/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/uprofound/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

# Foodgram - Продуктовый помощник

На этом сервисе пользователи смогут публиковать рецепты, подписываться на 
публикации других пользователей, добавлять понравившиеся рецепты в список 
«Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.  

Онлайн-сервис доступен по адресу: <http://62.84.127.196/>  
Документация по API: <http://62.84.127.196/api/docs/>

## Технологии:
Python 3.8.6 Django 3.0.5  
Django REST Framework  
Djoser PostgreSQL  
Docker gunicorn NGINX CI



## Запуск приложения локально в docker-контейнерах:

* Клонируйте репозиторий и перейдите в него в командной строке:

    ```bash
    git clone git@github.com:uprofound/foodgram-project-react.git
    cd foodgram-project-react
    ```

* Перейдите в каталог infra и подготовьте в нём файл переменных окружения .env:

    скопируйте шаблон из файла .env.template:  

    ```bash
    cd infra
    cp .env.template .env
    ```

    заполните его следующими данными:  
    
    ```
    SECRET_KEY='' # секретный ключ Django (укажите свой)
    POSTGRES_DB=postgres_db # имя базы данных (укажите своё)
    POSTGRES_USER=postgres # логин для подключения к базе данных (укажите свой)
    POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
    DB_HOST=db # название сервиса (контейнера)
    DB_PORT=5432 # порт для подключения к БД
  
    # Опционально:
    # DEBUG=True # default=False
    # ALLOWED_HOSTS=ip_your_server, backend, localhost, 127.0.0.1 # перечислить 
                    через запятую, default='backend, localhost'
    ```

* Установите docker и docker-compose:

    ```bash
    sudo apt install docker.io
    sudo apt install docker-compose
    ```
  
* Запустите приложение в docker-контейнерах:

    ```bash
    sudo docker-compose up -d
    ```

* Выполните миграции и сбор статики:

    ```bash
    sudo docker-compose exec backend python3 manage.py migrate --noinput
    sudo docker-compose exec backend python3 manage.py collectstatic --no-input
    ```

Теперь по адресу <http://localhost/api/docs/> доступна документация по API проекта.

### Создание суперпользователя

Для администрирования проекта используется суперпользователь. 
Для его создания выполните команду:

```bash
sudo docker-compose exec backend python3 manage.py createsuperuser
```

Теперь возможна авторизация по логину в админ-зоне по адресу <http://localhost/admin/>  
В самом приложении авторизация производится по email по адресу <http://localhost/signin/>

### Импорт списка ингредиентов

Для наполнения базы данных перечнем ингредиентов выполните команду:

```bash
sudo docker-compose exec backend python3 manage.py load_ingredients
```

### Остановка работы всех контейнеров

Выполните команду:

```bash
docker-compose down
```

Остановка работы контейнеров с удалением volumes и images:
```bash
docker-compose down --volumes --rmi
```
