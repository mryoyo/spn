"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from app_employee.views import work_line_report
from app_products.views import purchase_order_report
from .admin import custom_admin

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('app/', custom_admin.urls),
    path('report/work_line', work_line_report),
    path('report/purchase_order', purchase_order_report),
    path('', RedirectView.as_view(url=reverse_lazy('custom_admin:index'))),
]
