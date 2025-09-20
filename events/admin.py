from django.contrib import admin
from .models import Event, Category, RSVP


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_time', 'end_time', 'category')
    list_filter = ('category', 'start_time', 'end_time')
    search_fields = ('title', 'description', 'location')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'event__title')
