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
- Dashboard с бизнес метрики (rating и активност)
- Audit trail (`ActivityLog`) за ключови действия
- Bootstrap UI + custom CSS

### Права по роли
| Роля | Права |
| --- | --- |
| Anonymous | Достъп само до публични страници (`home`, `offers` list/detail), без private actions |
| Learner | Създава booking, отменя позволени booking-и, добавя/редактира/трие свое review, ползва favorites |
| Mentor | Създава/редактира/трие свои offers, вижда и обновява booking-и към своите offers |
| Superuser | Пълен достъп в admin + bypass в app views (manage all offers/bookings/reviews) |

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
- Dashboard with business metrics (rating and activity)
- Audit trail (`ActivityLog`) for important actions
- Bootstrap UI + custom CSS

### Role permissions
| Role | Permissions |
| --- | --- |
| Anonymous | Access to public pages only (`home`, `offers` list/detail), no private actions |
| Learner | Can create bookings, cancel allowed bookings, create/edit/delete own reviews, use favorites |
| Mentor | Can create/edit/delete own offers, view and update bookings for own offers |
| Superuser | Full admin access + bypass in app views (manage all offers/bookings/reviews) |

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


### Checks and tests
```bash
python manage.py check
python manage.py test
```
