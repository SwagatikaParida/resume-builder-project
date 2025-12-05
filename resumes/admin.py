from django.contrib import admin
from .models import Resume, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'location')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'owner', 'email', 'updated_at')
    search_fields = ('full_name', 'email', 'owner__username')
