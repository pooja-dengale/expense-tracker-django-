"""
Expenses app configuration.
Configures the expenses application for expense tracking.
"""

from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenses'
