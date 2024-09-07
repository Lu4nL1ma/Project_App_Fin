from django.contrib import admin
from financas_online import models


# Register your models here.

@admin.register(models.customers)
class CadastroCliente(admin.ModelAdmin):
    list_display = 'id', 'nome', 'cpf', 'telefone', 'nascimento',

@admin.register(models.cursos)
class Cadastrocursos(admin.ModelAdmin):
    list_display = 'id', 'curso',

@admin.register(models.turmas_formatec)
class Cadastroturmas(admin.ModelAdmin):
   list_display = 'id', 'turmas_formatec',

@admin.register(models.financas)
class financas(admin.ModelAdmin):
   list_display = 'id_ori','cliente', 'parcela', 'valor', 'data',


