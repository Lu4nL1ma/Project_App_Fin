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
