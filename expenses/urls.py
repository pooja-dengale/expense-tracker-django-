"""
URL routing for expenses app.
Maps URLs to expense and income management views.
"""

from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Expense URLs
    path('list/', views.ExpenseListView.as_view(), name='expense_list'),
    path('add/', views.ExpenseCreateView.as_view(), name='add_expense'),
    path('edit/<int:pk>/', views.ExpenseUpdateView.as_view(), name='edit_expense'),
    path('delete/<int:pk>/', views.ExpenseDeleteView.as_view(), name='delete_expense'),
    
    # Income URLs
    path('income/list/', views.IncomeListView.as_view(), name='income_list'),
    path('income/add/', views.IncomeCreateView.as_view(), name='add_income'),
    path('income/edit/<int:pk>/', views.IncomeUpdateView.as_view(), name='edit_income'),
    path('income/delete/<int:pk>/', views.IncomeDeleteView.as_view(), name='delete_income'),
    
    # Category URLs
    path('category/add/', views.CategoryCreateView.as_view(), name='add_category'),
    
    # Budget URLs
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/add/', views.BudgetCreateView.as_view(), name='add_budget'),
    path('budget/edit/<int:pk>/', views.BudgetUpdateView.as_view(), name='edit_budget'),
    path('budget/delete/<int:pk>/', views.BudgetDeleteView.as_view(), name='delete_budget'),
]
