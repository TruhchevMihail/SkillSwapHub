from rest_framework import serializers

from .models import SkillCategory, SkillOffer, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = ('id', 'name')


class OfferListSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SkillOffer
        fields = (
            'id',
            'title',
            'price_per_session',
            'duration_minutes',
            'level',
            'is_active',
            'owner',
            'category',
            'image',
        )


class OfferDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    category = SkillCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = SkillOffer
        fields = (
            'id',
            'title',
            'description',
            'price_per_session',
            'duration_minutes',
            'level',
            'image',
            'is_active',
            'created_at',
            'updated_at',
            'owner',
            'category',
            'tags',
        )

