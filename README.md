# FastAPI LLM service with JWT auth
## Описание
Серверное приложение на FastAPI с JWT аутентификацией, SQLite и интеграцией с LLM через OpenRouter.
## Технологии
- FastAPI
- JWT аутентификация
- SQLite + SQLAlchemy (асинхронный)
- OpenRouter API (GPT-4o-mini)
- uv (управление зависимостями)

### Установка и запуск

1. Клонирование репозитория

git clone https://github.com/NosulchakE/llm-p.git
cd llm-p

2. Настройка виртуального окружения
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows

3. Установка зависимостей

uv pip install -r <(uv pip compile pyproject.toml)

4. Настройка переменных окружения

cp .env.example .env

5. Запуск сервера

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Документация API
После запуска сервера Swagger доступен по адресу:

http://localhost:8000/docs

### Эндпоинты
Health Check
GET /health — проверка работоспособности сервера

Auth (аутентификация)
POST /auth/register — регистрация пользователя

POST /auth/login — получение JWT токена

GET /auth/me — получение профиля

Chat (требуют авторизации)
POST /chat — отправка запроса к LLM

GET /chat/history — получение истории диалога

DELETE /chat/history — очистка истории

### Демонстрация работы
1. Регистрация пользователя
https://screenshots/1_register.png

Email: nosulchak_elena@mail.ru

2. Логин и получение JWT токена
https://screenshots/2_login.png

3. Авторизация в Swagger
https://screenshots/3_authorize.png

Кнопка Authorize → ввод токена в формате Bearer <token>

4. Вызов POST /chat
https://screenshots/4_chat_request.png

Запрос:

json
{
  "prompt": "Расскажи короткую шутку про программистов"
}
Ответ:

json
{
  "answer": "Почему программисты любят природу? Потому что там много \"багов\"!"
}

5. Получение истории через GET /chat/history
https://screenshots/5_history.png

6. Удаление истории через DELETE /chat/history
https://screenshots/6_delete_history.png

База данных SQLite
Данные пользователей и история диалогов сохраняются в app.db:

bash
### Просмотр пользователей
sqlite3 app.db "SELECT id, email, role FROM users;"

### Просмотр истории
sqlite3 app.db "SELECT role, content FROM chat_messages LIMIT 5;"

Проверка кода
ruff check
Результат: All checks passed!
