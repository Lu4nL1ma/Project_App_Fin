from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

dir = FileSystemStorage(location='/fin_tech/media', base_url='/media/')

class cursos(models.Model):
    curso = models.CharField(max_length=50, default='não informado!')
    registro_curs = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.curso

class turmas_formatec(models.Model):
    turmas_formatec = models.CharField(max_length=40, default='não informado!')
    registro_turms = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.turmas_formatec

class customers(models.Model):
    nome = models.CharField(max_length=100, blank=False, default='não informado!')
    cpf = models.CharField(max_length=50, blank=False, default='não informado!')
    telefone = models.CharField(max_length=50, blank=False, default='não informado!')
    nascimento = models.DateField(auto_now=False, blank=False)
    registro_client = models.DateField(auto_now=True)

class financas(models.Model):
    id_ori = models.CharField(max_length=50, blank=False, default=' ')
    cliente = models.CharField(max_length=100, blank=False, default=' ')
    parcela = models.CharField(max_length=100, blank=False, default=' ')
    valor = models.CharField(max_length=100, blank=False, default=' ')
    curso = models.CharField(max_length=50, blank=False, default=' ')
    turma = models.CharField(max_length=50,blank=False, default=' ')
    vencimento = models.DateField(auto_now=False, null=True)
    data_pagamento = models.DateField(auto_now=False, null=True)
    banco = models.CharField(max_length=50, blank=False, default=' ')
    arquivo = models.ImageField(storage=dir, blank=True, default=' ')
    registro_fin = models.DateField(auto_now=True)

    

