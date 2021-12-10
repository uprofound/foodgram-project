Запуск приложения в docker-контейнерах:
docker-compose up -d --build

Проект станет доступен по адресу:
http://localhost

Создание суперюзера:
docker-compose exec backend python manage.py createsuperuser

Остановка работы контейнеров:
docker-compose down