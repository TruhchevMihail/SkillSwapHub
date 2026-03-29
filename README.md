# SkillSwap Hub

## Български

SkillSwap Hub е уеб приложение за обмен на умения между потребители. Всеки може да създава оферти за умения, да разглежда наличните предложения и да запазва любими.

### Основни функции
- Регистрация, вход и изход
- Създаване, редакция и изтриване на оферти
- Филтриране по категория, ниво и цена
- Любими оферти
- Админ панел за управление

### Технологии
- Django
- PostgreSQL (или SQLite за локални тестове)
- Django Template Engine
- Django TestCase

### Стартиране (локално)
```bash
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
cd SkillSwap-Hub
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Приложението ще е достъпно на `http://127.0.0.1:8000/`.

### Тестове
```bash
python manage.py test
```

## English

SkillSwap Hub is a web application for peer-to-peer skill exchange. Users can publish skill offers, browse available offers, and keep favorites.

### Main Features
- User registration, login, and logout
- Create, edit, and delete skill offers
- Filtering by category, level, and price
- Favorite offers
- Admin panel for management

### Tech Stack
- Django
- PostgreSQL (or SQLite for local testing)
- Django Template Engine
- Django TestCase

### Local Setup
```bash
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
cd SkillSwap-Hub
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

### Tests
```bash
python manage.py test
```
