from django.urls import path
from . import views

urlpatterns = [
     path('expense-analysis/', views.expense_analysis, name='expense_analysis'),
     
     
    
]


