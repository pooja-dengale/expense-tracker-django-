"""
Main URL router for the expense_tracker project.
Routes requests to accounts and expenses apps.
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('expenses.urls', namespace='expenses')),  # Include all expenses URLs at root
]
from django.conf import settings

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
