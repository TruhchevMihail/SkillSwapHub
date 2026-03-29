# SkillSwap Hub

A Django-based skill exchange platform where users can offer and book skill-sharing sessions.

## 📋 Project Overview

SkillSwap Hub is a peer-to-peer skill exchange platform that allows users to:
- Create and manage skill offers
- Browse and filter available skills
- Book sessions with mentors
- Leave reviews and ratings
- Build a portfolio of skills

## 🛠 Tech Stack

- **Backend**: Django 5.1+, Django REST Framework
- **Database**: PostgreSQL (configured via .env)
- **Frontend**: HTML5, Django Templates
- **Testing**: Django TestCase
- **Authentication**: Custom AppUser model
- **Task Queue**: Celery (planned)

## 📁 Project Structure

```
SkillSwap-Hub/
├── accounts/          # User authentication & profiles
├── core/              # Home page & core views
├── offers/            # Skill offers management (MAIN APP)
├── bookings/          # Session bookings
├── reviews/           # Ratings & reviews
├── SkillSwap_Hub/     # Project settings
├── templates/         # HTML templates
├── staticfiles/       # Static files (CSS, JS, images)
├── media/             # User uploads
├── manage.py
├── requirements.txt
└── .env               # Environment variables
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- pip & virtualenv
- PostgreSQL (for production) or SQLite (development)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/TruhchevMihail/SkillSwapHub.git
cd SkillSwap-Hub

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your settings
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Load sample data
python manage.py populate_sample_data
```

### 4. Run Development Server

```bash
python manage.py runserver
# Access at http://127.0.0.1:8000/
```

### 5. Access Admin Panel

```
http://127.0.0.1:8000/admin/
# Login with superuser credentials
```

## 📚 Main Features

### Users & Authentication
- ✅ Custom AppUser model with profile pictures
- ✅ User registration, login, logout
- ✅ Profile management

### Skill Offers (Core Feature)
- ✅ Create, edit, delete skill offers
- ✅ Categories and tags system
- ✅ Price per session
- ✅ Difficulty levels (Beginner, Intermediate, Advanced)
- ✅ Image uploads
- ✅ Filtering & sorting

### Favorites
- ✅ Add/remove offers to favorites
- ✅ View favorite offers list
- ✅ One-to-one favorite list per user

### Admin Interface
- ✅ Manage users
- ✅ Manage categories, tags, offers
- ✅ View materials & uploads
- ✅ Monitor favorites

## 🧪 Testing

Run all tests:
```bash
python manage.py test --verbosity=2
```

Run specific app tests:
```bash
python manage.py test offers  # Test offers app
python manage.py test accounts  # Test accounts app
```

**Current Test Coverage**:
- 41 total tests
- 35 tests for offers app
- Model validations, views, templates all tested

## 📝 Database Models

### 5 Core Models:

1. **SkillCategory** — Categories for offers (Programming, Design, Music, etc.)
2. **Tag** — Tags for offers (Python, Photoshop, Remote, etc.)
3. **SkillOffer** — Main model for skill offerings with:
   - Foreign Key to AppUser (owner)
   - Foreign Key to SkillCategory
   - Many-to-Many to Tag
   - Image field for offer pictures
   - Price, duration, level fields
   - Created/Updated timestamps

4. **Material** — Files/notes uploaded for offers
   - Foreign Key to SkillOffer
   - Foreign Key to AppUser (uploader)

5. **FavoriteList** — User's favorite offers
   - One-to-One relationship to AppUser
   - Many-to-Many to SkillOffer

## 🔗 URL Routes

| Route | View | Purpose |
|-------|------|---------|
| `/` | Home | Homepage |
| `/accounts/register/` | RegisterUserView | User registration |
| `/accounts/login/` | SignInView | User login |
| `/accounts/logout/` | SignOutView | User logout |
| `/offers/` | OfferListView | Browse all offers |
| `/offers/create/` | OfferCreateView | Create new offer |
| `/offers/<pk>/` | OfferDetailView | View offer details |
| `/offers/<pk>/edit/` | OfferUpdateView | Edit offer |
| `/offers/<pk>/delete/` | OfferDeleteView | Delete offer |
| `/offers/my-offers/` | MyOffersListView | View own offers |
| `/offers/favorites/` | FavoriteOffersListView | View favorites |
| `/offers/<pk>/favorite/` | ToggleFavoriteView | Add/remove favorite |
| `/admin/` | Django Admin | Admin panel |

## 🔐 Security Features

- ✅ LoginRequiredMixin for protected views
- ✅ Owner-only edit/delete protection
- ✅ CSRF token validation
- ✅ Secure user authentication
- ✅ Environment variable config (no hardcoded secrets)

## 📦 Environment Variables (.env)

```
# Core
SECRET_KEY=your-django-secret-key
DEBUG=True

# Database
DB_NAME=skillswapdb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Allowed hosts
ALLOWED_HOSTS=127.0.0.1,localhost
```

## 📲 Pages & Navigation

**Public Pages** (accessible without login):
- Home page
- Offers list (with filtering)
- Offer details
- Login page
- Register page

**Private Pages** (login required):
- Create offer
- My offers
- Favorite offers
- Edit/delete own offers

**Admin Pages**:
- User management
- Category management
- Tag management
- Offer management
- Material management

## 🚀 Deployment

The project is configured for deployment on:
- Heroku
- PythonAnywhere
- AWS (with RDS for PostgreSQL)
- DigitalOcean

See deployment guide in `docs/DEPLOYMENT.md` (coming soon)

## 📄 License

This project is for educational purposes (SoftUni Django Advanced Course).

## 👤 Author

Developed as part of SoftUni Django Advanced Regular Exam (2026)

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review GitHub issues
3. Check test files for usage examples

---

**Status**: ✅ Development in progress

**Current Phase**: Day 2 - Offers App Implementation Complete

