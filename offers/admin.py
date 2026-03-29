from django.contrib import admin

from .models import SkillCategory, Tag, SkillOffer, Material, FavoriteList


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(SkillOffer)
class SkillOfferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'owner',
        'category',
        'price_per_session',
        'level',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'level', 'is_active')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'offer', 'uploaded_by', 'uploaded_at')
    search_fields = ('title',)


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    filter_horizontal = ('offers',)


