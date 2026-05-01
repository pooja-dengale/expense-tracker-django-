"""
Custom error handlers for production.
Provides user-friendly error pages instead of generic 500 errors.
"""

from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound
import logging

logger = logging.getLogger(__name__)


def handler500(request):
    """
    Custom 500 error handler.
    Logs the error and shows a user-friendly page.
    """
    logger.error('Server Error (500)', exc_info=True, extra={
        'request': request,
    })
    
    return render(request, '500.html', status=500)


def handler404(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, '404.html', status=404)
