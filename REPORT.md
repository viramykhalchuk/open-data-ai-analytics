# REPORT — open-data-ai-analytics

## Посилання на репозиторій
https://github.com/viramykhalchuk/open-data-ai-analytics

## Мета роботи
Створено репозиторій для аналізу відкритих даних з data.gov.ua з розділенням розробки на модулі та роботою через feature-гілки і 
Pull Request. Реалізовано модулі завантаження даних, перевірки якості, дослідження та візуалізації. Додатково створено та 
розв’язано merge-конфлікт у README, додано changelog та створено тег релізу.

## Структура репозиторію
- README.md — опис проєкту, джерело даних, гіпотези
- .gitignore — ігнорування тимчасових файлів та великих даних (data/raw)
- data/README.md — опис даних (локальне зберігання великих файлів)
- src/ — код модулів:
  - data_load.py
  - data_quality_analysis.py
  - data_research.py
  - visualization.py
- reports/figures/ — збережені графіки (png)
- CHANGELOG.md — історія змін і реліз v0.1.0

## Хід виконання

### 1) Ініціалізація репозиторію та структура
Створено репозиторій `open-data-ai-analytics`, додано структуру папок і файлів за вимогами (README.md, .gitignore, 
data/README.md, notebooks/, src/, reports/figures/). Налаштовано `.gitignore` для ігнорування `__pycache__/`, 
`.ipynb_checkpoints/`, `.venv/`, `.env` та `data/raw/`. Зроблено коміт із базовою структурою.

### 2) Опис проєкту в README
Заповнено `README.md`: описано мету, додано посилання на джерело відкритих даних (data.gov.ua і ресурс набору даних), 
сформульовано 3 питання/гіпотези для аналізу. Зроблено окремий коміт.

### 3) Модуль data_load (feature/data_load)
Створено гілку `feature/data_load`. Додано скрипт `src/data_load.py`, який створює підвибірку `data/processed/sample_head.csv` з 
локального великого CSV-файлу (великий файл зберігається в `data/raw/` і не комітиться). Зміни змерджено в `main` через Pull 
Request.

### 4) Модуль data_quality_analysis (feature/data_quality_analysis)
Створено гілку `feature/data_quality_analysis`. Додано `src/data_quality_analysis.py` для перевірки якості даних (пропуски, 
дублікати, типи, базова статистика) на `data/processed/sample_head.csv`. Змерджено в `main` через Pull Request. Додатково 
виправлено читання CSV через авто-визначення розділювача (оскільки файл має розділювач `;`) — зміни змерджено окремим PR.

### 5) Модуль data_research (feature/data_research)
Створено гілку `feature/data_research`. Додано `src/data_research.py` з базовим дослідженням: preview даних, кількість 
унікальних значень, опис `MAKE_YEAR`, топ категорій (`BRAND`, `FUEL`, `KIND`, `COLOR`) та кореляція числових полів (`CAPACITY`, 
`OWN_WEIGHT`, `TOTAL_WEIGHT`). Змерджено в `main` через Pull Request.

### 6) Merge-конфлікт у README (пункт 9)
Створено дві гілки, які змінювали одну й ту саму секцію з гіпотезами у `README.md`. Після мерджу першої гілки в `main` виконано 
мердж другої гілки локально, отримано конфлікт у README та розв’язано його вручну з формуванням узгодженої фінальної версії. 
Результат закомічено та запушено в `main`.

### 7) Модуль visualization (feature/visualization)
Створено гілку `feature/visualization`. Додано `src/visualization.py`, який будує та зберігає графіки у `reports/figures/` (топ 
брендів, типи пального, топ кольорів, гістограма року випуску). Змерджено в `main` через Pull Request.

### 8) CHANGELOG та релізний тег
Додано `CHANGELOG.md` і створено тег `v0.1.0`, який вказує на коміт із changelog.


## git log --oneline --graph --decorate --all
vira@MacBook-Pro-Vira open-data-ai-analytics % git tag
git log --oneline --decorate -6
v0.1.0
1dd78cf (HEAD -> main, tag: v0.1.0, origin/main) Add changelog for v0.1.0
3f18b9e Merge pull request #6 from viramykhalchuk/feature/visualization
3996d65 (origin/feature/visualization, feature/visualization) Add visualization script
d5e1ef3 Resolve merge conflict in README hypotheses
836ed12 Merge pull request #5 from viramykhalchuk/conflict/hypotheses-a
2e97410 (origin/conflict/hypotheses-b, conflict/hypotheses-b) Update README hypotheses version B
vira@MacBook-Pro-Vira open-data-ai-analytics % git log --oneline --graph --decorate --all
* 1dd78cf (HEAD -> main, tag: v0.1.0, origin/main) Add changelog for v0.1.0
*   3f18b9e Merge pull request #6 from viramykhalchuk/feature/visualization
|\  
| * 3996d65 (origin/feature/visualization, feature/visualization) Add visualization script
|/  
*   d5e1ef3 Resolve merge conflict in README hypotheses
|\  
| * 2e97410 (origin/conflict/hypotheses-b, conflict/hypotheses-b) Update README hypotheses version B
* |   836ed12 Merge pull request #5 from viramykhalchuk/conflict/hypotheses-a
|\ \  
| |/  
|/|   
| * 966efe7 (origin/conflict/hypotheses-a, conflict/hypotheses-a) Update README hypotheses version A
|/  
*   d2667e4 Merge pull request #4 from viramykhalchuk/feature/data_research
|\  
| * d2488a4 (origin/feature/data_research, feature/data_research) Add data research script
|/  
*   a4fe341 Merge pull request #3 from viramykhalchuk/fix/csv-parsing
|\  
| * 0aa5336 (origin/fix/csv-parsing, fix/csv-parsing) Fix CSV delimiter detection in data quality analysis
|/  
*   b2f1d6b Merge pull request #2 from viramykhalchuk/feature/data_quality_analysis
|\  
| * 73cbc9c (origin/feature/data_quality_analysis, feature/data_quality_analysis) Add data quality analysis script
|/  
*   858c163 Merge pull request #1 from viramykhalchuk/feature/data_load
|\  
| * e7c6ec4 (origin/feature/data_load, feature/data_load) Add data_load script for local dataset sampling
* | b369df8 Update dataset link in README
|/  
* ed283c7 Add project description and analysis questions
* 94598c6 Init repository structure and gitignore
