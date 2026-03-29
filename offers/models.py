from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class SkillCategory(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.name


class SkillOffer(models.Model):
    LEVEL_BEGINNER = 'Beginner'
    LEVEL_INTERMEDIATE = 'Intermediate'
    LEVEL_ADVANCED = 'Advanced'

    LEVEL_CHOICES = [
        (LEVEL_BEGINNER, 'Beginner'),
        (LEVEL_INTERMEDIATE, 'Intermediate'),
        (LEVEL_ADVANCED, 'Advanced'),
    ]

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price_per_session = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    duration_minutes = models.PositiveIntegerField()

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=LEVEL_BEGINNER,
    )

    image = models.ImageField(
        upload_to='offer_images/',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill_offers',
    )

    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='offers',
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='offers',
    )

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if len(self.title.strip()) < 5:
            raise ValidationError({
                'title': 'Title must be at least 5 characters long.'
            })

        if self.price_per_session < 0:
            raise ValidationError({
                'price_per_session': 'Price cannot be negative.'
            })

        if self.duration_minutes < 15 or self.duration_minutes > 240:
            raise ValidationError({
                'duration_minutes': 'Duration must be between 15 and 240 minutes.'
            })

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('offer-detail', kwargs={'pk': self.pk})


class Material(models.Model):
    title = models.CharField(
        max_length=100,
    )

    file = models.FileField(
        upload_to='offer_materials/',
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    offer = models.ForeignKey(
        SkillOffer,
        on_delete=models.CASCADE,
        related_name='materials',
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_materials',
    )

    def __str__(self):
        return self.title


class FavoriteList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_list',
    )

    offers = models.ManyToManyField(
        SkillOffer,
        blank=True,
        related_name='favorited_by',
    )

    def __str__(self):
        return f"{self.user.username}'s favorites"

