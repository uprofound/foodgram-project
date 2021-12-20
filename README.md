[![foodgram_workflow](https://github.com/uprofound/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/uprofound/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

# praktikum_new_diplom

Для проверки работоспособности проекта есть возможность наполнить БД тестовыми данными и запустить приложение локально в тестовых docker-контейнерах.  

Для этого предварительно настройте виртуальное окружение, установите зависимости и выполнените миграции.

### Импорт тестовых данных

Перейдите в каталог backend и выполните команду:

```bash
python3 manage.py fill-data
```

Для загрузки дополнительных ингредиентов выполните команду:

```bash
python3 manage.py load_ingredients
```

## Запуск приложения локально в тестовых docker-контейнерах

Перейдите в каталог infra_dev.  

Запустите приложение в docker-контейнерах (выполняется со сборкой образа):

```bash
docker-compose up -d --build
```

Проект запустится по адресу <http://localhost/>,  
увидеть спецификацию API вы сможете по адресу <http://localhost/api/docs/>  

Создание суперюзера:
```bash
docker-compose exec backend python manage.py createsuperuser
```

Остановка работы контейнеров с удалением volumes и images:
```bash
docker-compose down --volumes --rmi local
```
