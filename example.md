error_report_app/
│
├── run.py                     # Точка входа: запуск Flask-приложения
├── config.py                  # Конфигурация приложения: секреты, база данных
├── init_db.py                 # Скрипт создания базы и супер-админа (Danderety)
├── requirements.txt           # Все зависимости проекта (Flask, SQLAlchemy и т.д.)
│	example.md

    .gitignore
├── app/
│   ├──____init____.py              # Создание и настройка Flask-приложения (app factory)
│   ├── models.py              # Модели базы данных: User, Ticket
│   ├── routes.py              # Flask-маршруты: логин, регистрация, заявки, админка
│   ├── forms.py               # Flask-WTF формы: логин, регистрация, отправка заявки
│   └── utils.py               # Вспомогательные функции: создание супер-админа и др.
│
├── templates/
│   ├── base.html              # Базовый шаблон с общими стилями и layout'ом
│   ├── login.html             # Страница входа в систему
│   ├── register.html          # Страница регистрации пользователя
│   ├── submit.html     # Форма отправки заявки (номер кабинета, категория и т.д.)
│   ├── admin_panel.html

    topbar.html

    users.html


│   └── users.html             # Список пользователей и кнопки “Сделать админом” (для Danderety)


│
└── static/

    icons/
			image.png
    ├── login.css              # Стили для страницы входа
    ├── register.css           # Стили для страницы регистрации
    ├── submit.css      # Стили для формы отправки заявки
    ├── admin_panel.css

    ├── base.css# Стили для админ-панели заявок


    └── users.css              # Стили для страницы управления пользователями

│		manifest.json

    sevice-worker.js
