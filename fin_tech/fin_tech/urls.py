"""
URL configuration for fin_tech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from financas_online import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('<int:c_id>/', views.customer, name='cliente'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls, name='admin'),  
    path('buscar/', views.buscar, name='buscar'),
    path('inserir/', views.inserir, name='inserir'),
    path('form/<int:c_id>/', views.form, name='form'),
    path('updatecli/<int:c_id>/', views.update_cliente, name='upcli'),
    path('updatefin/<int:c_id>/<int:f_id>/', views.updatefin, name='upfin'),   
]
