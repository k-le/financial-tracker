from django.urls import path
from .views import (
    TransactionDeleteView,
    TransactionListListView
    )
from . import views

urlpatterns = [
    path('', views.home, name='budgeter-home'),
    path('create/', views.create, name='budgeter-create'),
    path('dashboard/<int:id>', views.dashboard, name='budgeter-dashboard'),
    path('dashboard/my_budgets', TransactionListListView.as_view(), name='transactionlist-lists'),
    path('dashboard/transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete')
]
