from django.contrib import admin
from django.urls import path,include
from expenses import views
from django.contrib.auth import views as auth_views
from expenses import views as expense_views
urlpatterns = [

    path('admin/', admin.site.urls),
    path('', expense_views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('signup/', expense_views.signup, name='signup'),
    # login & logout (using Django’s built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Remove this line because it's already in expenses.urls
    # path('analysis/', views.expense_analysis, name='expense_analysis'),
    path('expenses/', include('expenses.urls')),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),


]


