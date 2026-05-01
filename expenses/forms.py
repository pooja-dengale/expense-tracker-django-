"""
Forms for expense and income management.
Handles validation for adding, editing expenses, incomes, budgets, and filtering.
"""

from django import forms
from django.forms import DateInput, NumberInput, TextInput
from .models import Expense, Category, Income, Budget
from datetime import datetime, timedelta


class CategoryForm(forms.ModelForm):
    """
    Form for creating and editing categories.
    """
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category name (e.g., Food, Transport, Entertainment)'
        })
    )

    class Meta:
        model = Category
        fields = ['name']


class ExpenseForm(forms.ModelForm):
    """
    Form for creating and editing expenses.
    Field attributes are styled for Bootstrap integration.
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Expense title (e.g., Lunch, Gas)'
        })
    )
    amount = forms.DecimalField(
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Amount',
            'step': '0.01'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional notes (optional)',
            'rows': 3
        })
    )

    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']

    def __init__(self, *args, user=None, **kwargs):
        """Initialize form and filter categories to only show user's categories."""
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)


class IncomeForm(forms.ModelForm):
    """
    Form for creating and editing income entries.
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Income title (e.g., Salary, Freelance Project)'
        })
    )
    amount = forms.DecimalField(
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Amount',
            'step': '0.01'
        })
    )
    income_type = forms.ChoiceField(
        choices=Income.INCOME_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional notes (optional)',
            'rows': 3
        })
    )

    class Meta:
        model = Income
        fields = ['title', 'amount', 'income_type', 'date', 'description']


class BudgetForm(forms.ModelForm):
    """
    Form for creating and editing budgets.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    limit = forms.DecimalField(
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Monthly limit',
            'step': '0.01'
        })
    )
    month = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text='First day of the month'
    )

    class Meta:
        model = Budget
        fields = ['category', 'limit', 'month']

    def __init__(self, *args, user=None, **kwargs):
        """Initialize form and filter categories to only show user's categories."""
        super().__init__(*args, **kwargs)
        self._user = user
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_month(self):
        """Normalize month to the first day of the selected month."""
        month = self.cleaned_data.get('month')
        if month:
            return month.replace(day=1)
        return month

    def clean_category(self):
        """Ensure the selected category belongs to the current user."""
        category = self.cleaned_data.get('category')
        if category and self._user and category.user != self._user:
            raise forms.ValidationError("Invalid category selection.")
        return category


class ExpenseFilterForm(forms.Form):
    """
    Form for filtering expenses by date range, category, and search term.
    """
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Category'
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title...'
        }),
        label='Search'
    )

    def __init__(self, *args, user=None, **kwargs):
        """Initialize with user's categories."""
        super().__init__(*args, **kwargs)
        self._user = user
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_category(self):
        """Ensure the selected category belongs to the current user."""
        category = self.cleaned_data.get('category')
        if category and self._user and category.user != self._user:
            raise forms.ValidationError("Invalid category selection.")
        return category


class IncomeFilterForm(forms.Form):
    """
    Form for filtering income by date range and income type.
    """
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )
    income_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Income.INCOME_TYPES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Income Type'
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title...'
        }),
        label='Search'
    )

    def __init__(self, *args, user=None, **kwargs):
        """Accept user parameter for API consistency (not used for income filtering)."""
        super().__init__(*args, **kwargs)

