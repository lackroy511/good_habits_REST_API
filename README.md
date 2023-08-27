# Habit Tracking Service

SPA application in which a user creates a habit they want to develop, specifying `time`, `place`, `action`, `interval`, and `duration`. It also integrates with the Telegram API for additional interaction. Users receive reminders in a Telegram chat about when it's time to perform the habit and notifications about the created habit.

## Tech Stack

- Django + DRF
- PostgreSQL
- Celery
- Redis
- Simple JWT
- Unittest
- Swagger (drf-yasg)
- CORS
- [Telegram API](https://core.telegram.org/bots/api)

## Installation and Running on Linux

1. Install Redis if not already installed: `sudo apt-get install redis`
2. Create a PostgreSQL database for the project.
3. Create and configure the `.env` file in the project root based on the `.env.sample` template.
4. From the project root in the terminal:
    - Install project dependencies: `poetry install`
    - Activate the virtual environment: `poetry shell`
    - Apply migrations: `python manage.py migrate`
    - Create a superuser if needed: `python manage.py createsuperuser` Default login: `1`, password: `1`
    - Create three terminal sessions and execute in each of them:
        - Start the server: `python manage.py runserver`
        - Start the celery worker: `celery -A config worker --loglevel=info`
        - Start the celery beat: `celery -A config beat --loglevel=info`
    - If the server is running locally, access the documentation at:
        - [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
        - [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## How It Works

A user registers, confirms their email address, becomes active, and can then log in, receiving an access token.

Using GET, POST, PUT, PATCH, DELETE, users can create habits in the database.

- Simultaneously selecting a connected habit and specifying a reward is not possible.
- The execution time should not exceed 120 seconds.
- Only enjoyable habits can be linked as connected habits.
- Enjoyable habits cannot have a reward or a connected habit.
- Habits cannot be scheduled less frequently than once every 7 days.
- A user cannot create a habit until they connect a Telegram bot.

After creating a habit, a celery task is created with for reminders.

the user receives a notification in their Telegram chat about the created habit.

Additionally, at the specified interval, the user receives a notification in their Telegram chat that it's time to perform the habit.
