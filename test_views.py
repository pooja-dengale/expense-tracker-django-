#!/usr/bin/env python
"""Quick test to verify views work correctly"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
os.environ['DEBUG'] = 'True'
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from expenses.views import DashboardView

# Create test user
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('testpass123')
    user.save()
    print("✓ Test user created")
else:
    print("✓ Test user exists")

# Test dashboard view
factory = RequestFactory()
request = factory.get('/')
request.user = user

view = DashboardView.as_view()
try:
    response = view(request)
    if response.status_code == 200:
        print("✓ Dashboard view works! Status: 200")
    else:
        print(f"✗ Dashboard returned status: {response.status_code}")
except Exception as e:
    print(f"✗ Dashboard view error: {e}")

print("\nTest complete! Try logging in with:")
print("Username: testuser")
print("Password: testpass123")
