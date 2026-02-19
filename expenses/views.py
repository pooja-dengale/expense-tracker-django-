"""
Views for expense and income management using Class-Based Views.
Handles CRUD operations, dashboard, filtering, pagination, and chart generation.
All views are protected with login_required to ensure user data isolation.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Q, F
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import Expense, Category, Income, Budget
from .forms import (
    ExpenseForm, IncomeForm, CategoryForm, BudgetForm,
    ExpenseFilterForm, IncomeFilterForm
)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/dashboard.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user expenses & incomes
        expenses = Expense.objects.filter(user=user).select_related('category')
        incomes = Income.objects.filter(user=user)

        # Calculate totals
        total_income = incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        total_expense = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        net_balance = total_income - total_expense

        # 🔹 COUNT EXPENSES
        expenses_count = expenses.count()

        # 🔹 CALCULATE AVERAGE EXPENSE (NEW CODE)
        if expenses_count > 0:
            average_expense = total_expense / expenses_count
        else:
            average_expense = Decimal('0.00')

        # Current month calculations
        current_date = timezone.now()
        month_start = current_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        month_expenses = expenses.filter(date__gte=month_start, date__lte=month_end)
        month_income = incomes.filter(date__gte=month_start, date__lte=month_end)

        month_total_expense = month_expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        month_total_income = month_income.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        context.update({
            'total_income': total_income,
            'total_expense': total_expense,
            'average_expense': average_expense,   # 👈 NEW
            'net_balance': net_balance,
            'abs_net_balance': abs(net_balance),
            'month_total_income': month_total_income,
            'month_total_expense': month_total_expense,
            'expenses_count': expenses_count,
        })

        return context

class ExpenseListView(LoginRequiredMixin, ListView):
    """
    Expense list view with pagination and filtering.
    """
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10
    login_url = 'accounts:login'

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user).select_related('category').order_by('-date')

        form = ExpenseFilterForm(self.request.GET, user=user)
        if form.is_valid():
            if form.cleaned_data.get('start_date'):
                queryset = queryset.filter(date__gte=form.cleaned_data['start_date'])
            if form.cleaned_data.get('end_date'):
                queryset = queryset.filter(date__lte=form.cleaned_data['end_date'])
            if form.cleaned_data.get('category'):
                queryset = queryset.filter(category=form.cleaned_data['category'])
            if form.cleaned_data.get('search'):
                queryset = queryset.filter(title__icontains=form.cleaned_data['search'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['filter_form'] = ExpenseFilterForm(self.request.GET, user=user)

        total = self.get_queryset().aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        context['total'] = total

        return context


class IncomeListView(LoginRequiredMixin, ListView):
    """
    Income list view with pagination, filtering, and search.
    Similar to ExpenseListView but for income entries.
    """
    model = Income
    template_name = 'expenses/income_list.html'
    context_object_name = 'incomes'
    paginate_by = 10
    login_url = 'accounts:login'

    def get_queryset(self):
        """Get filtered and paginated incomes for current user."""
        user = self.request.user
        queryset = Income.objects.filter(user=user).order_by('-date')

        # Apply filters
        form = IncomeFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('start_date'):
                queryset = queryset.filter(date__gte=form.cleaned_data['start_date'])
            if form.cleaned_data.get('end_date'):
                queryset = queryset.filter(date__lte=form.cleaned_data['end_date'])
            if form.cleaned_data.get('income_type'):
                queryset = queryset.filter(income_type=form.cleaned_data['income_type'])
            if form.cleaned_data.get('search'):
                queryset = queryset.filter(title__icontains=form.cleaned_data['search'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Add filter form
        context['filter_form'] = IncomeFilterForm(self.request.GET)
        
        # Add total for filtered incomes
        total = self.get_queryset().aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        context['total'] = total
        
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """
    Add expense view using CreateView.
    Automatically assigns expense to logged-in user.
    """
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/add_expense.html'
    success_url = reverse_lazy('expenses:dashboard')
    login_url = 'accounts:login'

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Assign expense to current user."""
        form.instance.user = self.request.user
        messages.success(self.request, '✓ Expense added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show error messages."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit expense view using UpdateView.
    Ensures user can only edit their own expenses.
    """
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/edit_expense.html'
    success_url = reverse_lazy('expenses:expense_list')
    login_url = 'accounts:login'

    def get_queryset(self):
        """Only allow access to user's own expenses."""
        return Expense.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Show success message."""
        messages.success(self.request, '✓ Expense updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show error messages."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete expense view using DeleteView.
    Ensures user can only delete their own expenses.
    """
    model = Expense
    template_name = 'expenses/delete_expense.html'
    success_url = reverse_lazy('expenses:expense_list')
    login_url = 'accounts:login'

    def get_queryset(self):
        """Only allow access to user's own expenses."""
        return Expense.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Show success message on delete."""
        messages.success(request, '✓ Expense deleted successfully!')
        return super().delete(request, *args, **kwargs)


class IncomeCreateView(LoginRequiredMixin, CreateView):
    """
    Add income view using CreateView.
    """
    model = Income
    form_class = IncomeForm
    template_name = 'expenses/add_income.html'
    success_url = reverse_lazy('expenses:dashboard')
    login_url = 'accounts:login'

    def form_valid(self, form):
        """Assign income to current user."""
        form.instance.user = self.request.user
        messages.success(self.request, '✓ Income added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show error messages."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit income view using UpdateView.
    """
    model = Income
    form_class = IncomeForm
    template_name = 'expenses/edit_income.html'
    success_url = reverse_lazy('expenses:income_list')
    login_url = 'accounts:login'

    def get_queryset(self):
        """Only allow access to user's own incomes."""
        return Income.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """Show success message."""
        messages.success(self.request, '✓ Income updated successfully!')
        return super().form_valid(form)


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete income view using DeleteView.
    """
    model = Income
    template_name = 'expenses/delete_income.html'
    success_url = reverse_lazy('expenses:income_list')
    login_url = 'accounts:login'

    def get_queryset(self):
        """Only allow access to user's own incomes."""
        return Income.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Show success message on delete."""
        messages.success(request, '✓ Income deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Add category view using CreateView.
    """
    model = Category
    form_class = CategoryForm
    template_name = 'expenses/add_category.html'
    success_url = reverse_lazy('expenses:dashboard')
    login_url = 'accounts:login'

    def form_valid(self, form):
        """Assign category to current user."""
        form.instance.user = self.request.user
        messages.success(self.request, '✓ Category added successfully!')
        return super().form_valid(form)


class BudgetListView(LoginRequiredMixin, ListView):
    """
    Budget list view showing all budgets and remaining amounts.
    """
    model = Budget
    template_name = 'expenses/budget_list.html'
    context_object_name = 'budgets'
    login_url = 'accounts:login'

    def get_queryset(self):
        """Get budgets for current user with category info."""
        return Budget.objects.filter(
            user=self.request.user
        ).select_related('category').order_by('-month')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add budget details with calculations
        budgets_with_details = []
        for budget in self.get_queryset():
            spent = budget.get_spent()
            remaining = budget.get_remaining()
            percentage = budget.get_percentage_used()
            
            budgets_with_details.append({
                'budget': budget,
                'remaining': remaining,
                'abs_remaining': abs(remaining),  
                'spent': spent,
                'percentage': percentage,
                'status':  'danger' if percentage >= 90 else (
        'warning' if percentage >= 70 else 'success'
    )            })
        
        context['budgets_with_details'] = budgets_with_details
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    """
    Create budget view using CreateView.
    """
    model = Budget
    form_class = BudgetForm
    template_name = 'expenses/add_budget.html'
    success_url = reverse_lazy('expenses:budget_list')
    login_url = 'accounts:login'

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Assign budget to current user."""
        form.instance.user = self.request.user
        messages.success(self.request, '✓ Budget created successfully!')
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update budget view using UpdateView.
    """
    model = Budget
    form_class = BudgetForm
    template_name = 'expenses/edit_budget.html'
    success_url = reverse_lazy('expenses:budget_list')
    login_url = 'accounts:login'

    def get_queryset(self):
        """Only allow access to user's own budgets."""
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Show success message."""
        messages.success(self.request, '✓ Budget updated successfully!')
        return super().form_valid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete budget view using DeleteView.
    """
    model = Budget
    template_name = 'expenses/delete_budget.html'
    success_url = reverse_lazy('expenses:budget_list')
    login_url = 'accounts:login'

    def get_queryset(self):
        """Only allow access to user's own budgets."""
        return Budget.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """Show success message on delete."""
        messages.success(request, '✓ Budget deleted successfully!')
        return super().delete(request, *args, **kwargs)
