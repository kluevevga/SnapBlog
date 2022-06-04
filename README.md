# SnapJournal

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&labelColor=333333&logo=python&logoColor=white)](https://www.python.org/)
[![flake8](https://img.shields.io/badge/code%20style-flake8-blue?style=for-the-badge&labelColor=333333)](https://flake8.pycqa.org/)
[![Django](https://img.shields.io/badge/Django-4.1.5-blue?style=for-the-badge&labelColor=333333&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Pillow](https://img.shields.io/badge/Pillow-9.4.0-blue?style=for-the-badge&labelColor=333333)](https://pillow.readthedocs.io/en/stable/index.html)
[![sorl-thumbnail](https://img.shields.io/badge/sorl%20thumbnail-12.7.0-blue?style=for-the-badge&labelColor=333333)](https://sorl-thumbnail.readthedocs.io/en/latest/)
[![Faker](https://img.shields.io/badge/Faker-12.0.1-blue?style=for-the-badge&labelColor=333333)](https://faker.readthedocs.io/en/master/)
[![Лицензия](https://img.shields.io/github/license/kluevevga/SnapJournal?color=blue&style=for-the-badge&labelColor=333333&logo=github)](https://github.com/kluevevga/SnapJournal/blob/master/LICENSE)
[![Размер кода](https://img.shields.io/github/languages/code-size/kluevevga/SnapJournal?style=for-the-badge&labelColor=333333&logo=github)](https://github.com/kluevevga/SnapJournal)

## О проекте 💻🚀

SnapJournal - это веб-платформа, разработанная с использованием Django, предназначенная для создания и
управления блогами. Он обладает богатым набором функциональных возможностей, которые включают в себя:

- Создание постов с возможностью вставки изображений 📸.
- Возможность подписываться на авторов и получать уведомления о их новых публикациях 📩.
- Добавление постов в избранное для быстрого доступа ⭐.
- Возможность комментирования постов и общения с другими пользователями 💬.
- Интегрированная система регистрации и восстановления пароля для пользователей 🔐.

Проект работает на серверной стороне, обеспечивая Server-Side Rendering (SSR) для веб-страниц. В основе его функционала
лежит Django, а данные хранятся в базе данных SQLite с использованием Django ORM. Для администрирования баз данных
предусмотрена административная панель.

Для обеспечения качества и надежности проекта были написаны тесты с использованием django-unittest, охватывающие
основные модули.

Этот проект представляет собой мощный инструмент для создания и управления вашими блогами, предоставляя полный спектр
возможностей для взаимодействия с вашей аудиторией. 🌟👨‍💻

## Установка

Клонировать проект

```shell
git clone https://github.com/kluevevga/SnapJournal
```

Перейти в проект и установить локальное окружение

```shell
cd  SnapJournal
python3 -m venv venv
```

Активировать окружение

```shell
venv\Scripts\activate              # windows(PowerShell)
source venv/Scripts/activate       # windows(Git Bash)
source venv/bin/activate           # linux(Bash)
```

Установить зависимости

```shell
pip3 install -r requirements.txt
```

Запустить миграции

```shell
python3 manage.py migrate
```

Запустить локальный сервер

```shell
py manage.py runserver
```

## Лицензия 📜

Этот проект распространяется под лицензией MIT. Дополнительную информацию можно найти в
файле [LICENSE](https://github.com/kluevevga/SnapJournal/blob/master/LICENSE).