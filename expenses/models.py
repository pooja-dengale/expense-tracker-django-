"""
Models for expense tracking.
Defines Category, Expense, Income, and Budget models for complete finance management.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Category(models.Model):
    """
    Category model for grouping expenses.
    Fields:
        - name: Category name (string)
        - user: Foreign key to User (owner of the category)
        - created_at: Timestamp when category was created
    """
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('shopping', 'Shopping'),
        ('groceries', 'Groceries'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.name


class Expense(models.Model):
    """
    Expense model for recording individual expenses.
    Uses select_related for optimized queries.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'category', '-date']),
        ]

    def __str__(self):
        return f"{self.title} - ${self.amount}"


class Income(models.Model):
    """
    Income model for recording income entries.
    Similar structure to Expense but for tracking income.
    """
    INCOME_TYPES = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('bonus', 'Bonus'),
        ('gift', 'Gift'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    income_type = models.CharField(max_length=20, choices=INCOME_TYPES, default='salary')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'income_type', '-date']),
        ]

    def __str__(self):
        return f"{self.title} - ${self.amount}"


class Budget(models.Model):
    """
    Budget model for tracking monthly spending limits per category.
    Calculates remaining balance automatically.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    month = models.DateField(help_text="First day of the month")
    limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-month']
        unique_together = ['user', 'category', 'month']
        indexes = [
            models.Index(fields=['user', '-month']),
            models.Index(fields=['user', 'category', '-month']),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.month.strftime('%B %Y')} - ${self.limit}"

    def get_spent(self):
        """Calculate total spent in this category for this month."""
        from django.db.models import Sum
        result = self.category.expenses.filter(
            user=self.user,
            date__year=self.month.year,
            date__month=self.month.month
        ).aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0.00')

    def get_remaining(self):
        """Calculate remaining budget for this month."""
        return self.limit - self.get_spent()

    def get_percentage_used(self):
        """Get percentage of budget used."""
        if self.limit == 0:
            return 0
        spent = self.get_spent()
        return min(int((spent / self.limit) * 100), 100)

