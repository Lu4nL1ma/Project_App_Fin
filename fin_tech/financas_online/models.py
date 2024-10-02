from django.db import models

# Create your models here.

class cursos(models.Model):
    curso = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.curso

class turmas_formatec(models.Model):
    turmas_formatec = models.CharField(max_length=40)
    def __str__(self) -> str:
        return self.turmas_formatec

class customers(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    cpf = models.CharField(max_length=50, blank=False)
    telefone = models.CharField(max_length=50, blank=False)
    nascimento = models.DateField(auto_now=False)
    registro = models.DateField(auto_now=True)

class financas(models.Model):
    id_ori = models.CharField(max_length=50)
    cliente = models.CharField(max_length=100)
    parcela = models.CharField(max_length=100)
    valor = models.CharField(max_length=100) 
    curso = models.CharField(max_length=50, blank=False)
    turma = models.CharField(max_length=50,blank=False)
    data = models.DateField(auto_now=False)
    arquivo = models.FileField(upload_to='posts/%Y/%m/%d/')
    

