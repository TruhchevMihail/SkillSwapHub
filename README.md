# SkillSwap Hub

SkillSwap Hub is a Django platform where mentors publish skill offers and learners book sessions.

---

## English

### 1) Project overview
SkillSwap Hub provides a complete learning-session flow:
- user registration and authentication
- mentor offers and learner bookings
- booking status lifecycle
- post-session reviews
- REST API endpoints (DRF)
- async background tasks (Celery)

### 2) Main features
- Authentication: register, login, logout
- Role-based access with Django groups: `Mentors`, `Learners`
- Offers: create, edit, delete, list, detail
- Favorites (saved offers)
- Bookings with statuses: `Pending`, `Approved`, `Rejected`, `Cancelled`, `Completed`
- Reviews allowed only for completed bookings
- User profile page + profile editing + password change
- Dashboard with counters and recent activity
- API endpoints for offers and bookings
- Celery tasks for reminders and stale booking cleanup

### 3) Tech stack
- Python, Django 6
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Cloudinary (media)
- WhiteNoise (static in production)
- Bootstrap 5

### 4) Quick start (Windows PowerShell)
```powershell
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
Set-Location SkillSwap-Hub

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`, then run:

```powershell
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

### 5) Optional demo data
```powershell
python populate_sample_data.py
```

### 6) Environment variables (`.env`)
Use `.env.example` and fill all values.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` or `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated origins with scheme (`https://...`) |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `CLOUDINARY_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `CELERY_BROKER_URL` | Celery broker URL (Redis) |
| `CELERY_RESULT_BACKEND` | Celery result backend URL |

### 7) API endpoints
Base URLs are configured in `SkillSwap_Hub/urls.py`.

Public:
- `GET /api/offers/`
- `GET /api/offers/<id>/`

Authenticated:
- `POST /api/bookings/create/<offer_id>/`
- `GET /api/bookings/my/`

### 8) Run Celery
Start Redis first, then run worker:

```powershell
celery -A SkillSwap_Hub worker --loglevel=info
```

Optional beat scheduler:

```powershell
celery -A SkillSwap_Hub beat --loglevel=info
```

### 9) Roles and permissions
This project relies on Django groups.

Create/update base groups with:

```powershell
python manage.py setup_groups
```

Default groups used in access checks:
- `Mentors`
- `Learners`

### 10) Tests and checks
```powershell
python manage.py check
python manage.py test
```

### 11) Helpful commands
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 12) Troubleshooting
- **Static/CSS missing in production**: run `collectstatic` and verify static settings.
- **Cloudinary error (`Must supply cloud_name`)**: verify Cloudinary env vars.
- **CSRF trusted origins error**: ensure origins start with `http://` or `https://`.
- **Celery not processing tasks**: check Redis is running and worker is started.

### 13) Links
- Live app: `https://skillswaphub-csbyhgeucparhxcb.spaincentral-01.azurewebsites.net`
- Repository: `https://github.com/TruhchevMihail/SkillSwapHub.git`

---

## Български

### 1) Обща информация
SkillSwap Hub е Django платформа, в която ментори публикуват оферти, а обучаеми резервират сесии.

Проектът включва пълен поток:
- регистрация и вход
- оферти и резервации
- статуси на booking-и
- reviews след завършена сесия
- REST API (DRF)
- асинхронни задачи с Celery

### 2) Основни функционалности
- Аутентикация: регистрация, вход, изход
- Роли чрез Django групи: `Mentors`, `Learners`
- Оферти: създаване, редакция, изтриване, списък, детайли
- Любими оферти
- Booking статуси: `Pending`, `Approved`, `Rejected`, `Cancelled`, `Completed`
- Review само за completed booking
- Публичен профил + редакция на профил + смяна на парола
- Dashboard със статистики и activity
- API endpoints за offers и bookings
- Celery задачи за reminder-и и cleanup

### 3) Технологии
- Python, Django 6
- Django REST Framework
- PostgreSQL
- Celery + Redis
- Cloudinary (медия)
- WhiteNoise (static в production)
- Bootstrap 5

### 4) Бърз старт локално (Windows PowerShell)
```powershell
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
Set-Location SkillSwap-Hub

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
Copy-Item .env.example .env
```

Редактирай `.env`, после изпълни:

```powershell
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

Отвори: `http://127.0.0.1:8000/`

### 5) По желание: демо данни
```powershell
python populate_sample_data.py
```

### 6) Environment променливи (`.env`)
Използвай `.env.example` и попълни всички стойности.

| Променлива | Описание |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` или `False` |
| `ALLOWED_HOSTS` | Списък от хостове, разделени със запетая |
| `CSRF_TRUSTED_ORIGINS` | Списък от origins със схема (`https://...`) |
| `DB_NAME` | Име на PostgreSQL база |
| `DB_USER` | PostgreSQL потребител |
| `DB_PASSWORD` | PostgreSQL парола |
| `DB_HOST` | PostgreSQL host |
| `DB_PORT` | PostgreSQL port |
| `CLOUDINARY_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `CELERY_BROKER_URL` | URL на Celery broker (Redis) |
| `CELERY_RESULT_BACKEND` | URL на Celery result backend |

### 7) API endpoints
Маршрутите са вързани в `SkillSwap_Hub/urls.py`.

Публични:
- `GET /api/offers/`
- `GET /api/offers/<id>/`

За логнат потребител:
- `POST /api/bookings/create/<offer_id>/`
- `GET /api/bookings/my/`

### 8) Пускане на Celery
Първо стартирай Redis, после worker:

```powershell
celery -A SkillSwap_Hub worker --loglevel=info
```

По желание beat scheduler:

```powershell
celery -A SkillSwap_Hub beat --loglevel=info
```

### 9) Роли и права
Проектът използва Django групи.

Създай/обнови базовите групи с:

```powershell
python manage.py setup_groups
```

Използвани групи:
- `Mentors`
- `Learners`

### 10) Тестове и проверки
```powershell
python manage.py check
python manage.py test
```

### 11) Полезни команди
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 12) Чести проблеми
- **Липсва CSS в production**: изпълни `collectstatic` и провери static настройките.
- **Cloudinary грешка (`Must supply cloud_name`)**: провери Cloudinary env променливите.
- **CSRF trusted origins грешка**: origins трябва да започват с `http://` или `https://`.
- **Celery не изпълнява задачи**: провери дали Redis и worker са стартирани.

### 13) Линкове
- Live app: `https://skillswaphub-csbyhgeucparhxcb.spaincentral-01.azurewebsites.net`
- Repository: `https://github.com/TruhchevMihail/SkillSwapHub.git`
