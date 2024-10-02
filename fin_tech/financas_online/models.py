from django.db import models

# Create your models here.

class cursos(models.Model):
    curso = models.CharField(max_length=50, default='não informado!')
    registro = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.curso

class turmas_formatec(models.Model):
    turmas_formatec = models.CharField(max_length=40, default='não informado!')
    registro = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.turmas_formatec

class customers(models.Model):
    nome = models.CharField(max_length=100, blank=False, default='não informado!')
    cpf = models.CharField(max_length=50, blank=False, default='não informado!')
    telefone = models.CharField(max_length=50, blank=False, default='não informado!')
    nascimento = models.DateField(auto_now=False, default='DD-MM-YYYY')
    registro = models.DateField(auto_now=True)

class financas(models.Model):
    id_ori = models.CharField(max_length=50, blank=False, default='não informado!')
    cliente = models.CharField(max_length=100, blank=False, default='não informado!')
    parcela = models.CharField(max_length=100, blank=False, default='não informado!')
    valor = models.CharField(max_length=100, blank=False, default='não informado!')
    curso = models.CharField(max_length=50, blank=False, default='não informado!')
    turma = models.CharField(max_length=50,blank=False, default='não informado!')
    data = models.DateField(auto_now=False, default='DD-MM-YYYY')
    data_pagamento = models.DateField(auto_now=False, default='DD-MM-YYYY')
    banco = models.CharField(max_length=50, blank=False, default='não informado!')
    arquivo = models.FileField(upload_to='posts/%Y/%m/%d/', blank=True, default='não informado!')
    registro = models.DateField(auto_now=True)

    

