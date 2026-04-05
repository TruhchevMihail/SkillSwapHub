from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from offers.models import SkillCategory, SkillOffer

from .models import Booking


UserModel = get_user_model()


class BookingModelAndApiTests(TestCase):
	def setUp(self):
		self.mentor = UserModel.objects.create_user(username='mentor', password='pass12345')
		self.learner = UserModel.objects.create_user(username='learner', password='pass12345')
		self.other_learner = UserModel.objects.create_user(username='otherlearner', password='pass12345')
		self.category = SkillCategory.objects.create(name='Programming')
		self.offer = SkillOffer.objects.create(
			title='Learn Python Well',
			description='Python mentoring sessions',
			price_per_session=Decimal('55.00'),
			duration_minutes=60,
			owner=self.mentor,
			category=self.category,
		)

	def test_booking_model_requires_future_date(self):
		booking = Booking(
			offer=self.offer,
			learner=self.learner,
			preferred_date=timezone.now() - timedelta(hours=1),
		)

		with self.assertRaises(ValidationError):
			booking.full_clean()

	def test_booking_model_cannot_book_own_offer(self):
		booking = Booking(
			offer=self.offer,
			learner=self.mentor,
			preferred_date=timezone.now() + timedelta(days=1),
		)

		with self.assertRaises(ValidationError):
			booking.full_clean()

	def test_booking_create_api_requires_authentication(self):
		response = self.client.post(
			reverse('api-booking-create', kwargs={'offer_pk': self.offer.pk}),
			data={
				'preferred_date': (timezone.now() + timedelta(days=1)).isoformat(),
				'message': 'I want to learn.',
			},
		)

		self.assertIn(response.status_code, {401, 403})

	def test_booking_create_api_creates_booking_for_authenticated_user(self):
		self.client.force_login(self.learner)

		response = self.client.post(
			reverse('api-booking-create', kwargs={'offer_pk': self.offer.pk}),
			data={
				'preferred_date': (timezone.now() + timedelta(days=2)).isoformat(),
				'message': 'Please book me.',
			},
		)

		self.assertEqual(response.status_code, 201)
		booking = Booking.objects.get()
		self.assertEqual(booking.learner, self.learner)
		self.assertEqual(booking.offer, self.offer)
		self.assertEqual(booking.status, Booking.Status.PENDING)

	def test_my_bookings_api_returns_only_current_user_bookings(self):
		own_booking = Booking.objects.create(
			offer=self.offer,
			learner=self.learner,
			preferred_date=timezone.now() + timedelta(days=3),
			message='My booking',
		)
		Booking.objects.create(
			offer=self.offer,
			learner=self.other_learner,
			preferred_date=timezone.now() + timedelta(days=4),
			message='Other booking',
		)

		self.client.force_login(self.learner)
		response = self.client.get(reverse('api-my-bookings'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 1)
		self.assertEqual(response.json()[0]['id'], own_booking.pk)

