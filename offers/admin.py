from django.contrib import admin
from .models import Offer, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'offer', 'rating', 'date')
