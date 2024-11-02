from django.contrib import admin
from django.urls import path
from financas_online import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [   
    path('accounts/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:c_id>/', views.customer, name='cliente'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls, name='admin'),  
    path('buscar/', views.buscar, name='buscar'),
    path('inserir/', views.inserir, name='inserir'),
    path('curso/', views.curso, name='curso'),
    path('turma/', views.turma, name='turma'),
    path('form/<int:c_id>/', views.form, name='form'),
    path('updatecli/<int:c_id>/', views.update_cliente, name='upcli'),
    path('updatefin/<int:c_id>/<int:f_id>/', views.updatefin, name='upfin'),
    path('download_recibo/<int:c_id>/<int:f_id>', views.download_recibo, name='download_recibo'),
    path('dashboard_financeiro/', views.dashboard_financeiro, name='dash_f')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)