"""
Admin configuration for expenses app.
Registers Expense, Income, Category, and Budget models for Django admin interface.
"""

from django.contrib import admin
from .models import Expense, Category, Income, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model.
    Displays and manages expense categories.
    """
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'user__username']
    list_filter = ['created_at', 'user']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin interface for Expense model.
    Displays and manages individual expenses.
    """
    list_display = ['title', 'amount', 'category', 'user', 'date', 'created_at']
    search_fields = ['title', 'user__username']
    list_filter = ['category', 'date', 'user']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """
    Admin interface for Income model.
    Displays and manages individual income entries.
    """
    list_display = ['title', 'amount', 'income_type', 'user', 'date', 'created_at']
    search_fields = ['title', 'user__username']
    list_filter = ['income_type', 'date', 'user']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """
    Admin interface for Budget model.
    Displays and manages monthly budgets.
    """
    list_display = ['category', 'user', 'month', 'limit', 'get_spent', 'get_remaining']
    search_fields = ['category__name', 'user__username']
    list_filter = ['month', 'user', 'category']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_spent(self, obj):
        """Display amount spent."""
        return f"${obj.get_spent()}"
    get_spent.short_description = 'Spent'
    
    def get_remaining(self, obj):
        """Display remaining budget."""
        return f"${obj.get_remaining()}"
    get_remaining.short_description = 'Remaining'
