from django.contrib import admin
from financas_online import models


# Register your models here.

@admin.register(models.customers)
class CadastroCliente(admin.ModelAdmin):
    list_display = 'id', 'nome', 'cpf', 'telefone', 'nascimento', 'registro_client'

@admin.register(models.cursos)
class Cadastrocursos(admin.ModelAdmin):
    list_display = 'id', 'curso', 'registro_curs'

@admin.register(models.turmas_formatec)
class Cadastroturmas(admin.ModelAdmin):
   list_display = 'id', 'turmas_formatec', 'registro_turms'

@admin.register(models.financas)
class financas(admin.ModelAdmin):
   list_display = 'id','id_ori','cliente', 'parcela', 'valor', 'vencimento', 'data_pagamento', 'banco', 'arquivo', 'registro_fin'


