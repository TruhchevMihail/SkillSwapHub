# SkillSwap Hub

A Django platform for skill sharing between mentors and learners.

---

## English

### 1) Project overview
SkillSwap Hub is a web application where mentors create skill offers and learners book sessions.
It covers a full flow: registration -> offers -> bookings -> completed session -> review.
The project also includes REST API endpoints and Celery async tasks.

### 2) Main features
- Registration, login, logout
- User roles with Django Groups (`Mentors`, `Learners`)
- Offer CRUD (owner-only checks)
- Favorites
- Booking flow with statuses (Pending, Approved, Rejected, Cancelled, Completed)
- Reviews only for completed bookings
- Dashboard and activity tracking
- DRF API for offers and bookings
- Celery tasks for reminders and stale booking cleanup

### 3) Tech stack
- Python
- Django 6
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Cloudinary
- WhiteNoise
- Bootstrap 5
- Azure App Service

### 4) Local setup
```powershell
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
Set-Location SkillSwap-Hub
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

### 5) Sample data
```powershell
python populate_sample_data.py
```

### 6) Environment variables
Create `.env` based on `.env.example`.

Required keys:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `CLOUDINARY_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

### 7) API endpoints
Public:
- `GET /api/offers/`
- `GET /api/offers/<id>/`

Authenticated:
- `POST /api/bookings/create/<offer_id>/`
- `GET /api/bookings/my/`

### 8) Celery
Run worker:
```powershell
celery -A SkillSwap_Hub worker --loglevel=info
```

Run beat (optional):
```powershell
celery -A SkillSwap_Hub beat --loglevel=info
```

### 9) Tests
```powershell
python manage.py check
python manage.py test
```

### 10) Links
- Live app: `https://skillswaphub-csbyhgeucparhxcb.spaincentral-01.azurewebsites.net`
- Repository: `https://github.com/TruhchevMihail/SkillSwapHub.git`

---

## Български

### 1) Обща информация
SkillSwap Hub е уеб платформа за обмен на умения между ментори и обучаеми.
Проектът покрива пълен flow: регистрация -> оферти -> booking -> завършена сесия -> review.
Има и REST API + Celery async задачи.

### 2) Основни функционалности
- Регистрация, вход, изход
- Роли чрез Django Groups (`Mentors`, `Learners`)
- CRUD за оферти (owner-only проверки)
- Любими оферти
- Booking flow със статуси (Pending, Approved, Rejected, Cancelled, Completed)
- Reviews само за completed bookings
- Dashboard и activity tracking
- DRF API за offers и bookings
- Celery задачи за напомняния и cleanup на стари booking-и

### 3) Технологии
- Python
- Django 6
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Cloudinary
- WhiteNoise
- Bootstrap 5
- Azure App Service

### 4) Локално стартиране
```powershell
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
Set-Location SkillSwap-Hub
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

### 5) Примерни данни
```powershell
python populate_sample_data.py
```

### 6) Environment променливи
Направи `.env` файл по `.env.example`.

Нужни ключове:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `CLOUDINARY_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

### 7) API endpoints
Публични:
- `GET /api/offers/`
- `GET /api/offers/<id>/`

Само за логнат потребител:
- `POST /api/bookings/create/<offer_id>/`
- `GET /api/bookings/my/`

### 8) Celery
Worker:
```powershell
celery -A SkillSwap_Hub worker --loglevel=info
```

Beat (по желание):
```powershell
celery -A SkillSwap_Hub beat --loglevel=info
```

### 9) Тестове
```powershell
python manage.py check
python manage.py test
```

### 10) Линкове
- Live app: `https://skillswaphub-csbyhgeucparhxcb.spaincentral-01.azurewebsites.net`
- Repository: `https://github.com/TruhchevMihail/SkillSwapHub.git`
