# SkillSwap Hub

## Български

SkillSwap Hub е платформа за обмен на умения между **ментори** и **обучаеми**.
Проектът е изграден с Django и покрива пълен flow:
оферти -> booking -> completed session -> review.

### Основни функционалности
- Разширен потребителски модел (`AppUser`)
- Регистрация, вход, изход
- Роли чрез **Groups**: `Mentors`, `Learners`
- CRUD за оферти (owner-only защити)
- Booking flow със статуси и role checks
- Reviews за завършени booking-и (1 review на booking)
- Dashboard с бизнес метрики (rating, completion rate, response time)
- Audit trail (`ActivityLog`) за ключови действия
- Export команда за данни (JSON/CSV)
- Bootstrap UI + custom CSS

### Технологии
- Django 6
- Django REST Framework
- PostgreSQL
- Celery / Redis (подготвени dependency-и)

### Локално стартиране
```bash
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
cd SkillSwap-Hub
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

### Seed sample data
```bash
python populate_sample_data.py
```

Sample users (password: `testpass123`):
- `mentor1`, `mentor2`
- `learner1`, `learner2`

### Export данни
```bash
python manage.py export_data
```

По подразбиране файловете се записват в `scripts/exports/`.

### Тестове и проверки
```bash
python manage.py check
python manage.py test
```

---

## English

SkillSwap Hub is a skill-sharing platform between **mentors** and **learners**.
It implements a full workflow:
offers -> booking -> completed session -> review.

### Key features
- Extended user model (`AppUser`)
- Registration, login, logout
- Role system via **Groups**: `Mentors`, `Learners`
- Offer CRUD with owner-only restrictions
- Booking flow with status transitions and role checks
- Reviews for completed bookings (1 review per booking)
- Dashboard with business metrics (rating, completion rate, response time)
- Audit trail (`ActivityLog`) for important actions
- Data export command (JSON/CSV)
- Bootstrap UI + custom CSS

### Tech stack
- Django 6
- Django REST Framework
- PostgreSQL
- Celery / Redis (dependencies prepared)

### Local setup
```bash
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
cd SkillSwap-Hub
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_groups
python manage.py createsuperuser
python manage.py runserver
```

### Seed sample data
```bash
python populate_sample_data.py
```

Sample users (password: `testpass123`):
- `mentor1`, `mentor2`
- `learner1`, `learner2`

### Export data
```bash
python manage.py export_data
```

By default files are saved to `scripts/exports/`.

### Checks and tests
```bash
python manage.py check
python manage.py test
```
