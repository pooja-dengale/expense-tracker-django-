"""
Models for accounts app.
Currently using Django's built-in User model via auth.contrib.
Custom user model can be extended here if needed.
"""

from django.db import models
from django.contrib.auth.models import User

# Using Django's built-in User model for authentication
# Can be extended with custom fields via Profile model if needed
