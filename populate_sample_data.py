import os
import sys
import django
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkillSwap_Hub.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import Group
from django.core.management import call_command
from accounts.models import AppUser
from offers.models import FavoriteList, SkillCategory, SkillOffer, Tag
from bookings.models import Booking
from reviews.models import Review


def create_users():
    users = {}
    data = [
        ('mentor1',  'mentor1@example.com',  'Alex',    'Turner'),
        ('mentor2',  'mentor2@example.com',  'Sara',    'Blake'),
        ('learner1', 'learner1@example.com', 'Jordan',  'Mills'),
        ('learner2', 'learner2@example.com', 'Taylor',  'Cruz'),
    ]
    for username, email, first, last in data:
        user, created = AppUser.objects.get_or_create(
            username=username,
            defaults={'email': email, 'first_name': first, 'last_name': last},
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f'  Created user: {username}')
        else:
            print(f'  User already exists: {username}')
        users[username] = user

    mentors_group, _ = Group.objects.get_or_create(name='Mentors')
    learners_group, _ = Group.objects.get_or_create(name='Learners')

    mentor_usernames = {'mentor1', 'mentor2'}
    for username, user in users.items():
        user.groups.clear()
        if username in mentor_usernames:
            user.groups.add(mentors_group)
        else:
            user.groups.add(learners_group)

    return users


def create_categories():
    cats = {}
    data = [
        ('Programming', 'Coding, software development, and computer science.'),
        ('Design',      'Graphic design, UI/UX, and visual communication.'),
        ('Music',       'Instruments, theory, singing, and production.'),
        ('Languages',   'Foreign language learning and conversation practice.'),
        ('Fitness',     'Physical training, yoga, nutrition, and wellness.'),
    ]
    for name, desc in data:
        cat, created = SkillCategory.objects.get_or_create(name=name, defaults={'description': desc})
        cats[name] = cat
        if created:
            print(f'  Created category: {name}')
    return cats


def create_tags():
    tags = {}
    names = ['Python', 'Django', 'JavaScript', 'Photoshop', 'Figma',
             'Guitar', 'Piano', 'Beginner Friendly', 'Remote', 'Advanced']
    for name in names:
        tag, created = Tag.objects.get_or_create(name=name)
        tags[name] = tag
        if created:
            print(f'  Created tag: {name}')
    return tags


def create_offers(users, cats, tags):
    offers_data = [
        {
            'title': 'Python for Absolute Beginners',
            'description': 'We will cover variables, loops, functions and basic data structures. No prior experience needed — just bring curiosity.',
            'price_per_session': '25.00',
            'duration_minutes': 60,
            'level': SkillOffer.LEVEL_BEGINNER,
            'owner': users['mentor1'],
            'category': cats['Programming'],
            'tags': ['Python', 'Beginner Friendly', 'Remote'],
        },
        {
            'title': 'Django REST Framework — Build Real APIs',
            'description': 'Learn to design and build production-ready REST APIs using Django REST Framework. We cover serializers, views, authentication, and permissions.',
            'price_per_session': '45.00',
            'duration_minutes': 90,
            'level': SkillOffer.LEVEL_INTERMEDIATE,
            'owner': users['mentor1'],
            'category': cats['Programming'],
            'tags': ['Python', 'Django'],
        },
        {
            'title': 'Figma UI Design from Scratch',
            'description': 'Practical UI/UX design using Figma. Learn components, auto-layout, prototyping, and how to hand off designs to developers.',
            'price_per_session': '35.00',
            'duration_minutes': 60,
            'level': SkillOffer.LEVEL_BEGINNER,
            'owner': users['mentor2'],
            'category': cats['Design'],
            'tags': ['Figma', 'Beginner Friendly'],
        },
        {
            'title': 'Acoustic Guitar — First Steps',
            'description': 'Learn to hold the guitar, basic chords, and your first songs. Ideal for complete beginners who want to play real music fast.',
            'price_per_session': '20.00',
            'duration_minutes': 45,
            'level': SkillOffer.LEVEL_BEGINNER,
            'owner': users['mentor2'],
            'category': cats['Music'],
            'tags': ['Guitar', 'Beginner Friendly'],
        },
        {
            'title': 'Spanish Conversation Practice',
            'description': 'Improve your spoken Spanish through real conversations, vocabulary drills, and pronunciation corrections. B1/B2 level welcome.',
            'price_per_session': '18.00',
            'duration_minutes': 50,
            'level': SkillOffer.LEVEL_INTERMEDIATE,
            'owner': users['mentor1'],
            'category': cats['Languages'],
            'tags': ['Remote'],
        },
        {
            'title': 'Advanced JavaScript & Async Patterns',
            'description': 'Deep dive into closures, event loop, promises, async/await, and modern JavaScript patterns used in production frontend codebases.',
            'price_per_session': '50.00',
            'duration_minutes': 90,
            'level': SkillOffer.LEVEL_ADVANCED,
            'owner': users['mentor2'],
            'category': cats['Programming'],
            'tags': ['JavaScript', 'Advanced'],
        },
    ]

    created_offers = {}
    for data in offers_data:
        tag_names = data.pop('tags')
        offer, created = SkillOffer.objects.get_or_create(
            title=data['title'],
            owner=data['owner'],
            defaults=data,
        )
        if created:
            offer.tags.set([tags[t] for t in tag_names if t in tags])
            print(f'  Created offer: {offer.title}')
        else:
            print(f'  Offer already exists: {offer.title}')
        created_offers[offer.title] = offer
    return created_offers


def create_bookings(users, offers):
    now = timezone.now()
    bookings_data = [
        {
            'offer_title':    'Python for Absolute Beginners',
            'learner':        users['learner1'],
            'preferred_date': now + timedelta(days=5),
            'message':        'I am completely new to programming. Looking forward to starting!',
            'status':         Booking.Status.APPROVED,
        },
        {
            'offer_title':    'Acoustic Guitar — First Steps',
            'learner':        users['learner1'],
            'preferred_date': now + timedelta(days=10),
            'message':        'I have always wanted to play guitar. No experience at all.',
            'status':         Booking.Status.PENDING,
        },
        {
            'offer_title':    'Django REST Framework — Build Real APIs',
            'learner':        users['learner2'],
            'preferred_date': now + timedelta(days=7),
            'message':        'I know basic Django. Want to learn DRF for my next project.',
            'status':         Booking.Status.PENDING,
        },
        {
            'offer_title':    'Figma UI Design from Scratch',
            'learner':        users['learner2'],
            'preferred_date': now + timedelta(days=3),
            'message':        '',
            'status':         Booking.Status.REJECTED,
        },
        {
            'offer_title':    'Spanish Conversation Practice',
            'learner':        users['learner1'],
            'preferred_date': now - timedelta(days=10),
            'message':        'Great session, really enjoyed the conversation practice.',
            'status':         Booking.Status.COMPLETED,
        },
        {
            'offer_title':    'Advanced JavaScript & Async Patterns',
            'learner':        users['learner2'],
            'preferred_date': now - timedelta(days=5),
            'message':        'Exactly what I needed to understand async/await deeply.',
            'status':         Booking.Status.COMPLETED,
        },
    ]

    for data in bookings_data:
        offer = offers.get(data['offer_title'])
        if not offer:
            continue
        exists = Booking.objects.filter(offer=offer, learner=data['learner']).exists()
        if not exists:
            Booking.objects.create(
                offer=offer,
                learner=data['learner'],
                preferred_date=data['preferred_date'],
                message=data['message'],
                status=data['status'],
            )
            print(f'  Created booking: {data["learner"].username} → {data["offer_title"]} ({data["status"]})')
        else:
            print(f'  Booking already exists: {data["learner"].username} → {data["offer_title"]}')


def create_favorites(users, offers):
    fav_data = {
        'learner1': ['Django REST Framework — Build Real APIs', 'Figma UI Design from Scratch'],
        'learner2': ['Python for Absolute Beginners', 'Acoustic Guitar — First Steps'],
    }
    for username, titles in fav_data.items():
        user = users[username]
        fav_list, _ = FavoriteList.objects.get_or_create(user=user)
        for title in titles:
            offer = offers.get(title)
            if offer:
                fav_list.offers.add(offer)
                print(f'  {username} saved: {title}')


def create_reviews(users, offers):
    reviews_data = [
        {
            'offer_title': 'Spanish Conversation Practice',
            'learner':     users['learner1'],
            'rating':      5,
            'comment':     'Alex was incredibly patient and the session felt completely natural. My confidence in speaking Spanish improved a lot.',
        },
        {
            'offer_title': 'Advanced JavaScript & Async Patterns',
            'learner':     users['learner2'],
            'rating':      4,
            'comment':     'Sara explained closures and the event loop really clearly. A few examples could be more practical, but overall a great session.',
        },
    ]

    for data in reviews_data:
        offer = offers.get(data['offer_title'])
        if not offer:
            continue
        booking = Booking.objects.filter(
            offer=offer, learner=data['learner'], status=Booking.Status.COMPLETED
        ).first()
        if not booking:
            continue
        if hasattr(booking, 'review'):
            print(f'  Review already exists for: {data["offer_title"]}')
            continue
        Review.objects.create(
            booking=booking,
            author=data['learner'],
            mentor=offer.owner,
            rating=data['rating'],
            comment=data['comment'],
        )
        print(f'  Created review: {data["learner"].username} → {data["offer_title"]} ({data["rating"]}/5)')


if __name__ == '__main__':
    call_command('setup_groups')

    print('\n--- Users ---')
    users = create_users()

    print('\n--- Categories ---')
    cats = create_categories()

    print('\n--- Tags ---')
    tags = create_tags()

    print('\n--- Offers ---')
    offers = create_offers(users, cats, tags)

    print('\n--- Bookings ---')
    create_bookings(users, offers)

    print('\n--- Favourites ---')
    create_favorites(users, offers)

    print('\n--- Reviews ---')
    create_reviews(users, offers)

    print('\nDone! Test credentials: mentor1 / mentor2 / learner1 / learner2  (password: testpass123)')
