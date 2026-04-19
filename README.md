# 
open-data-ai-analytics

## Назва і мета
Мета проєкту — завантажити набір відкритих даних з порталу data.gov.ua, 
перевірити якість даних, виконати базове дослідження та побудувати 
візуалізації для отримання аналітичних висновків.

## Джерело відкритих даних
Портал відкритих даних України (data.gov.ua).  
Ресурс набору даних: 
https://data.gov.ua/dataset/06779371-308f-42d7-895e-5a39833375f0/resource/b1bcb4a9-8e60-4a1c-91c0-00faae008816

## Питання / гіпотези для аналізу
1. Які марки та категорії транспортних засобів найчастіше зустрічаються у вибірці даних?
2. Які типи пального та кольори є найпоширенішими серед транспортних засобів?
3. Чи існує зв’язок між роком випуску, вантажопідйомністю, власною масою та повною масою транспортного 
засобу?

## Docker Workspace

### Сервіси проєкту
- `db` — PostgreSQL база даних
- `data_load` — зчитування CSV і завантаження даних у БД
- `data_quality_analysis` — перевірка якості даних і формування JSON-звіту
- `data_research` — базове дослідження даних і формування JSON-звіту
- `visualization` — побудова графіків і збереження їх у PNG
- `web` — Flask-вебінтерфейс для перегляду результатів

### Структура
- `data_load/` — Dockerfile, app.py, requirements.txt для сервісу завантаження
- `data_quality_analysis/` — Dockerfile, app.py, requirements.txt для перевірки якості
- `data_research/` — Dockerfile, app.py, requirements.txt для дослідження
- `visualization/` — Dockerfile, app.py, requirements.txt для побудови графіків
- `web/` — Dockerfile, app.py, templates для веб-інтерфейсу
- `compose.yaml` — спільний запуск усіх сервісів

### Запуск
```bash
docker compose up --build
```

### Зупинка
```bash
docker compose down
```

### Доступ
- Веб-інтерфейс: `http://localhost:8000`
- PostgreSQL: порт `5432`

### Взаємодія сервісів
- `data_load` імпортує CSV у PostgreSQL
- `data_quality_analysis` читає дані з БД і формує `quality_report.json`
- `data_research` читає дані з БД і формує `research_report.json`
- `visualization` читає дані з БД і формує PNG-графіки
- `web` показує таблицю даних, звіти та графіки через браузер
