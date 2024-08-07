"""office_emp_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# emp_app/urls.py

# office_emp_proj/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("index/", views.index, name="index"),
    path('all_emp/', views.all_emp, name='all_emp'),
    path("add_emp/", views.add_emp, name="add_emp"),
    path("remove_emp/", views.remove_emp, name="remove_emp"), 
    path("remove_emp/<int:emp_id>/", views.remove_emp, name="remove_emp_detail"), 
    path("filter_emp/", views.filter_emp, name="filter_emp"),
    path("update_emp/<int:emp_id>/", views.update_emp, name="update_emp"),
]


