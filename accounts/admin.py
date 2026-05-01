"""
Admin configuration for accounts app.
Registers models for Django admin interface.
"""

from django.contrib import admin
from django.contrib.auth.models import User

# Django User model is already registered in default admin
admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker"
