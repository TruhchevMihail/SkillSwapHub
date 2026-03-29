"""Tests for the offers app."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import SkillCategory, Tag, SkillOffer, Material, FavoriteList

User = get_user_model()


class SkillCategoryTests(TestCase):
    """Test cases for SkillCategory model."""

    def setUp(self):
        self.category = SkillCategory.objects.create(
            name='Programming',
            description='Programming courses'
        )

    def test_category_creation(self):
        """Test that a category can be created."""
        self.assertEqual(self.category.name, 'Programming')
        self.assertEqual(self.category.description, 'Programming courses')

    def test_category_str(self):
        """Test the string representation of a category."""
        self.assertEqual(str(self.category), 'Programming')

    def test_category_name_is_unique(self):
        """Test that category names must be unique."""
        with self.assertRaises(Exception):
            SkillCategory.objects.create(name='Programming')


class TagTests(TestCase):
    """Test cases for Tag model."""

    def setUp(self):
        self.tag = Tag.objects.create(name='Python')

    def test_tag_creation(self):
        """Test that a tag can be created."""
        self.assertEqual(self.tag.name, 'Python')

    def test_tag_str(self):
        """Test the string representation of a tag."""
        self.assertEqual(str(self.tag), 'Python')

    def test_tag_name_is_unique(self):
        """Test that tag names must be unique."""
        with self.assertRaises(Exception):
            Tag.objects.create(name='Python')


class SkillOfferTests(TestCase):
    """Test cases for SkillOffer model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            level=SkillOffer.LEVEL_BEGINNER,
            owner=self.user,
            category=self.category
        )

    def test_offer_creation(self):
        """Test that an offer can be created."""
        self.assertEqual(self.offer.title, 'Learn Python')
        self.assertEqual(self.offer.owner, self.user)
        self.assertTrue(self.offer.is_active)

    def test_offer_str(self):
        """Test the string representation of an offer."""
        self.assertEqual(str(self.offer), 'Learn Python')

    def test_offer_get_absolute_url(self):
        """Test the get_absolute_url method."""
        url = self.offer.get_absolute_url()
        self.assertEqual(url, reverse('offer-detail', kwargs={'pk': self.offer.pk}))

    def test_offer_title_too_short_raises_error(self):
        """Test that title validation works."""
        invalid_offer = SkillOffer(
            title='Test',
            description='Description',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            invalid_offer.full_clean()

    def test_offer_negative_price_raises_error(self):
        """Test that negative price validation works."""
        invalid_offer = SkillOffer(
            title='Valid Title',
            description='Description',
            price_per_session=Decimal('-10.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            invalid_offer.full_clean()

    def test_offer_duration_validation(self):
        """Test that duration must be between 15 and 240 minutes."""
        invalid_offer = SkillOffer(
            title='Valid Title',
            description='Description',
            price_per_session=Decimal('50.00'),
            duration_minutes=500,
            owner=self.user,
            category=self.category
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            invalid_offer.full_clean()

    def test_offer_tags_m2m(self):
        """Test many-to-many relationship with tags."""
        tag1 = Tag.objects.create(name='Python')
        tag2 = Tag.objects.create(name='Beginner')
        self.offer.tags.add(tag1, tag2)
        self.assertEqual(self.offer.tags.count(), 2)
        self.assertIn(tag1, self.offer.tags.all())


class MaterialTests(TestCase):
    """Test cases for Material model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )

    def test_material_creation(self):
        """Test that a material can be created."""
        material = Material.objects.create(
            title='Python Guide',
            file='materials/guide.pdf',
            offer=self.offer,
            uploaded_by=self.user
        )
        self.assertEqual(material.title, 'Python Guide')
        self.assertEqual(material.offer, self.offer)
        self.assertEqual(material.uploaded_by, self.user)

    def test_material_str(self):
        """Test the string representation of a material."""
        material = Material.objects.create(
            title='Python Guide',
            file='materials/guide.pdf',
            offer=self.offer,
            uploaded_by=self.user
        )
        self.assertEqual(str(material), 'Python Guide')


class FavoriteListTests(TestCase):
    """Test cases for FavoriteList model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer1 = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )
        self.offer2 = SkillOffer.objects.create(
            title='Learn JavaScript',
            description='A comprehensive JavaScript course',
            price_per_session=Decimal('45.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )

    def test_favorite_list_creation(self):
        """Test that a favorite list is created for a user."""
        fav_list = FavoriteList.objects.create(user=self.user)
        self.assertEqual(fav_list.user, self.user)

    def test_favorite_list_str(self):
        """Test the string representation of a favorite list."""
        fav_list = FavoriteList.objects.create(user=self.user)
        self.assertEqual(str(fav_list), f"{self.user.username}'s favorites")

    def test_favorite_list_add_offers(self):
        """Test adding offers to a favorite list."""
        fav_list = FavoriteList.objects.create(user=self.user)
        fav_list.offers.add(self.offer1, self.offer2)
        self.assertEqual(fav_list.offers.count(), 2)

    def test_favorite_list_one_to_one(self):
        """Test that each user has only one favorite list."""
        fav_list1 = FavoriteList.objects.create(user=self.user)
        with self.assertRaises(Exception):
            FavoriteList.objects.create(user=self.user)


class OfferListViewTests(TestCase):
    """Test cases for OfferListView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category,
            is_active=True
        )

    def test_offer_list_view_returns_200(self):
        """Test that the offer list view returns 200."""
        response = self.client.get(reverse('offer-list'))
        self.assertEqual(response.status_code, 200)

    def test_offer_list_view_uses_correct_template(self):
        """Test that the correct template is used."""
        response = self.client.get(reverse('offer-list'))
        self.assertTemplateUsed(response, 'offers/offer-list.html')

    def test_offer_list_view_contains_offers(self):
        """Test that the offer list contains offers."""
        response = self.client.get(reverse('offer-list'))
        self.assertIn(self.offer, response.context['offers'])


class OfferDetailViewTests(TestCase):
    """Test cases for OfferDetailView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )

    def test_offer_detail_view_returns_200(self):
        """Test that the offer detail view returns 200."""
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_offer_detail_view_uses_correct_template(self):
        """Test that the correct template is used."""
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        self.assertTemplateUsed(response, 'offers/offer-detail.html')

    def test_offer_detail_view_contains_offer(self):
        """Test that the detail page contains the offer."""
        response = self.client.get(reverse('offer-detail', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.context['offer'], self.offer)


class OfferCreateViewTests(TestCase):
    """Test cases for OfferCreateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')

    def test_offer_create_requires_login(self):
        """Test that creating an offer requires login."""
        response = self.client.get(reverse('offer-create'))
        self.assertNotEqual(response.status_code, 200)

    def test_offer_create_view_returns_200_when_logged_in(self):
        """Test that the offer create view returns 200 when logged in."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('offer-create'))
        self.assertEqual(response.status_code, 200)

    def test_offer_create_view_uses_correct_template(self):
        """Test that the correct template is used."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('offer-create'))
        self.assertTemplateUsed(response, 'offers/offer-create.html')

    def test_offer_create_post_creates_offer(self):
        """Test that posting creates a new offer."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Learn JavaScript',
            'description': 'JavaScript course',
            'price_per_session': Decimal('40.00'),
            'duration_minutes': 60,
            'level': SkillOffer.LEVEL_BEGINNER,
            'category': self.category.pk,
        }
        response = self.client.post(reverse('offer-create'), data)
        self.assertEqual(SkillOffer.objects.filter(title='Learn JavaScript').count(), 1)


class OfferUpdateViewTests(TestCase):
    """Test cases for OfferUpdateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )

    def test_offer_update_requires_login(self):
        """Test that updating an offer requires login."""
        response = self.client.get(reverse('offer-edit', kwargs={'pk': self.offer.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test_owner_can_update_offer(self):
        """Test that the owner can update their offer."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('offer-edit', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_update_offer(self):
        """Test that non-owner cannot update someone else's offer."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('offer-edit', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, 404)


class OfferDeleteViewTests(TestCase):
    """Test cases for OfferDeleteView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.category = SkillCategory.objects.create(name='Programming')
        self.offer = SkillOffer.objects.create(
            title='Learn Python',
            description='A comprehensive Python course',
            price_per_session=Decimal('50.00'),
            duration_minutes=60,
            owner=self.user,
            category=self.category
        )

    def test_offer_delete_requires_login(self):
        """Test that deleting an offer requires login."""
        response = self.client.get(reverse('offer-delete', kwargs={'pk': self.offer.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test_owner_can_delete_offer(self):
        """Test that the owner can delete their offer."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('offer-delete', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_delete_offer(self):
        """Test that non-owner cannot delete someone else's offer."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('offer-delete', kwargs={'pk': self.offer.pk}))
        self.assertEqual(response.status_code, 404)

