from django.contrib import admin
from .models import User, HealthRecord

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('full_name', 'email_address', 'date_of_birth')

    # Adds a search bar to search by name or email
    search_fields = ('full_name', 'email_address')

    # Optional: Adds filters on the right sidebar
    list_filter = ('date_of_birth',)


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('user', 'glucose', 'haemoglobin', 'cholesterol','remarks', 'created_at')

    # Adds filters on the right sidebar
    list_filter = ('created_at',)

    # Allows searching by the related User's full_name
    search_fields = ('user__full_name',)