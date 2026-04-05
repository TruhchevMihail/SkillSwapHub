# SkillSwap Hub

 SkillSwap Hub is a Django platform for skill sharing between mentors and learners.

---

## English

### Overview
SkillSwap Hub allows mentors to create offers and learners to book sessions.
The app covers a full flow: registration, offers, bookings, completed session, and review.
It also includes REST API endpoints and Celery async tasks.

### Main Features
- Registration, login, logout
- User roles via Django Groups (`Mentors`, `Learners`)
- Offer CRUD with owner-only access checks
- Favorites list
- Booking flow with statuses: `Pending`, `Approved`, `Rejected`, `Cancelled`, `Completed`
- Reviews only for completed bookings
- Dashboard and activity tracking
- DRF API for offers and bookings
- Celery tasks for reminders and stale booking cleanup

### Tech Stack
- Python
- Django 6
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Cloudinary
- WhiteNoise
- Bootstrap 5
- Azure App Service

### Local Setup (Windows PowerShell)
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

### Optional: Populate Sample Data
```powershell
python populate_sample_data.py
```

### Environment Variables
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

### API Endpoints
Public:
- `GET /api/offers/`
- `GET /api/offers/<id>/`

Authenticated:
- `POST /api/bookings/create/<offer_id>/`
- `GET /api/bookings/my/`

### Celery
Run worker:
```powershell
celery -A SkillSwap_Hub worker --loglevel=info
```

Run beat (optional):
```powershell
celery -A SkillSwap_Hub beat --loglevel=info
```

### Tests
```powershell
python manage.py check
python manage.py test
```

### Links
- Live app: `https://skillswaphub-csbyhgeucparhxcb.spaincentral-01.azurewebsites.net`
- Repository: `https://github.com/TruhchevMihail/SkillSwapHub.git`

---

## Български

### Обща информация
SkillSwap Hub е Django платформа за обмен на умения между ментори и обучаеми.
Проектът покрива пълен flow: регистрация, оферти, booking, завършена сесия и review.
Има и REST API endpoints и Celery async задачи.

### Основни функционалности
- Регистрация, вход, изход
- Роли чрез Django Groups (`Mentors`, `Learners`)
- CRUD за оферти с owner-only проверки
- Любими оферти
- Booking flow със статуси: `Pending`, `Approved`, `Rejected`, `Cancelled`, `Completed`
- Reviews само за completed bookings
- Dashboard и activity tracking
- DRF API за offers и bookings
- Celery задачи за напомняния и cleanup на стари booking-и

### Технологии
- Python
- Django 6
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Cloudinary
- WhiteNoise
- Bootstrap 5
- Azure App Service

### Локално стартиране (Windows PowerShell)
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

### По желание: Примерни данни
```powershell
python populate_sample_data.py
```

### Environment променливи
Създай `.env` по `.env.example`.

Необходими ключове:
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

### API Endpoints
Публични:
- `GET /api/offers/`
- `GET /api/offers/<id>/`

Само за логнат потребител:
- `POST /api/bookings/create/<offer_id>/`
- `GET /api/bookings/my/`

### Celery
Worker:
```powershell
celery -A SkillSwap_Hub worker --loglevel=info
```

Beat (по желание):
```powershell
celery -A SkillSwap_Hub beat --loglevel=info
```

### Тестове
```powershell
python manage.py check
python manage.py test
```

### Линкове
- Live app: `https://skillswaphub-csbyhgeucparhxcb.spaincentral-01.azurewebsites.net`
- Repository: `https://github.com/TruhchevMihail/SkillSwapHub.git`
