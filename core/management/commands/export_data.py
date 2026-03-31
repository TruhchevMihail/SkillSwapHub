import csv
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from bookings.models import Booking
from offers.models import SkillOffer
from reviews.models import Review


class Command(BaseCommand):
    help = 'Export offers, bookings and reviews to JSON and CSV files.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--out-dir',
            type=str,
            default=str(Path(settings.BASE_DIR) / 'scripts' / 'exports'),
            help='Output folder for exported files.',
        )

    def handle(self, *args, **options):
        out_dir = Path(options['out_dir'])
        out_dir.mkdir(parents=True, exist_ok=True)

        self._export_offers(out_dir)
        self._export_bookings(out_dir)
        self._export_reviews(out_dir)

        self.stdout.write(self.style.SUCCESS(f'Export finished: {out_dir}'))

    def _export_offers(self, out_dir: Path):
        offers = SkillOffer.objects.select_related('owner', 'category').prefetch_related('tags')

        offers_json = []
        for offer in offers:
            offers_json.append({
                'id': offer.id,
                'title': offer.title,
                'owner': offer.owner.username,
                'category': offer.category.name,
                'price_per_session': str(offer.price_per_session),
                'duration_minutes': offer.duration_minutes,
                'level': offer.level,
                'is_active': offer.is_active,
                'tags': [tag.name for tag in offer.tags.all()],
                'created_at': offer.created_at.isoformat(),
            })

        (out_dir / 'offers.json').write_text(json.dumps(offers_json, indent=2), encoding='utf-8')

        with (out_dir / 'offers.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id', 'title', 'owner', 'category', 'price_per_session',
                'duration_minutes', 'level', 'is_active', 'tags', 'created_at',
            ])
            for item in offers_json:
                writer.writerow([
                    item['id'], item['title'], item['owner'], item['category'],
                    item['price_per_session'], item['duration_minutes'],
                    item['level'], item['is_active'], ', '.join(item['tags']), item['created_at'],
                ])

    def _export_bookings(self, out_dir: Path):
        bookings = Booking.objects.select_related('offer', 'offer__owner', 'learner')

        booking_rows = []
        for booking in bookings:
            booking_rows.append({
                'id': booking.id,
                'offer': booking.offer.title,
                'mentor': booking.offer.owner.username,
                'learner': booking.learner.username,
                'status': booking.status,
                'preferred_date': booking.preferred_date.isoformat(),
                'created_at': booking.created_at.isoformat(),
            })

        (out_dir / 'bookings.json').write_text(json.dumps(booking_rows, indent=2), encoding='utf-8')

        with (out_dir / 'bookings.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'offer', 'mentor', 'learner', 'status', 'preferred_date', 'created_at'])
            for item in booking_rows:
                writer.writerow([
                    item['id'], item['offer'], item['mentor'], item['learner'],
                    item['status'], item['preferred_date'], item['created_at'],
                ])

    def _export_reviews(self, out_dir: Path):
        reviews = Review.objects.select_related('author', 'mentor', 'booking', 'booking__offer')

        review_rows = []
        for review in reviews:
            review_rows.append({
                'id': review.id,
                'offer': review.booking.offer.title,
                'author': review.author.username,
                'mentor': review.mentor.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat(),
            })

        (out_dir / 'reviews.json').write_text(json.dumps(review_rows, indent=2), encoding='utf-8')

        with (out_dir / 'reviews.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'offer', 'author', 'mentor', 'rating', 'comment', 'created_at'])
            for item in review_rows:
                writer.writerow([
                    item['id'], item['offer'], item['author'], item['mentor'],
                    item['rating'], item['comment'], item['created_at'],
                ])

