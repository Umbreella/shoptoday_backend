# FastAPI Test task

![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![sqlalchemy](https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlite&logoColor=white)
![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Testing

![pytest](https://img.shields.io/badge/pytest_asyncio-2496ED?style=for-the-badge&logo=pytest&logoColor=white)
![codecov](https://img.shields.io/codecov/c/github/Umbreella/fastapi_test_task?style=for-the-badge&logo=codecov)

## Description

[Task Description](TaskDescription.pdf)

Completed items:

1. User can:
    1. :white_check_mark: Registration (login + password)
    2. :white_check_mark: Authorization (login + password)
    3. :white_check_mark: Viewing the list of products
    4. :white_check_mark: Purchase of goods if there is a sufficient amount of
       funds on the account
    5. :white_check_mark: View the balance of all accounts and transaction
       history
    6. :white_check_mark: Crediting funds to the account
2. Admin can:
    1. :white_check_mark: View all products
    2. :white_check_mark: View all users and their billing accounts
    3. :white_check_mark: Enabling/disabling users
    4. :white_check_mark: Create/edit/delete products
3. Non-functional criteria:
    1. :white_check_mark: User logins are unique
    2. :white_check_mark: After registration, the user is created in an
       inactive state.
    3. :white_check_mark: Authorization was made via JWT.

## Getting Started

### Dependencies

![postgresql](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

### Environment variables

* To run the application:
    * add in **environment variables** path to **.env** file
    * overwrite **.env** file
* The list of all environment variables is specified in the **[.env](.env)**

## Docker

1. docker-compose.yml

```docker
version: "3"

services:
    fastapi_test_task:
        image: umbreella/fastapi_test_task:latest
        ports:
            - [your_port]:8000
        environment:
            - ENV_FILE=[env_file]
        volumes:
            - [path_to_env_file]:/usr/src/app/[env_file]
```

* Docker-compose run

```commandline
docker-compose up -d
```

* Open bash in container

```commandline
docker exec --it fastapi_test_task bash
```

* Run commands

```commandline
alembic upgrade head
```

## Endpoints

* API docs

```commandline
[your_ip_address]/api/docs/
```

## Live Demo

* [https://shoptoday.umbreella-dev.ru/](https://shoptoday.umbreella-dev.ru/api/docs/)

