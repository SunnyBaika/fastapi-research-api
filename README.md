# FastAPI Research API

Этот API выполняет:
- Поиск информации через Google Search
- Анализ текста с помощью OpenAI GPT
- Генерацию PDF-отчёта

## Установка
1. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
2. Запустите сервер:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
