from financas_online.models import customers, financas
from financas_online.models import customers, financas, cursos
from django.forms import ModelForm
from django import forms

#CREATE YOUR FORMS HERE!

class customerform(ModelForm):
   class Meta:
      model = customers
      fields = '__all__'
      labels = {'nome':'Nome', 'cpf':'CPF', 'telefone':'Telefone', 'nascimento':'Data de Nascimento'}
      widgets = {
            'nome': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Insira o nome.'}),
            'cpf': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Insira o CPF.'}),
            'telefone': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Insira o Telefone.'}),
            'nascimento': forms.DateInput(attrs={'type': 'date',}),
        }
      
class inserir(ModelForm):
   class Meta: 
      Model = cursos
      fields = ['curso']
      widgets = { 'curso': forms.TextInput(attrs={'type': 'text',})}
      
class parcelaform(ModelForm):
   class Meta:
      model = financas
      fields = ['id_ori', 'cliente', 'parcela', 'valor', 'curso', 'turma', 'vencimento']
      parcelas = [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)]
      widgets = {
            'id_ori': forms.TextInput(attrs={'type': 'hidden',}),
            'cliente': forms.TextInput(attrs={'type': 'hidden',}),
            'parcela': forms.Select(choices=parcelas),
            'valor': forms.TextInput(attrs={'type': 'text',}),
            'curso': forms.Select(attrs={}),
            'turma': forms.Select(attrs={}),
            'vencimento': forms.DateInput(attrs={'type': 'date',}),
        }
      
class updtparcelaform(ModelForm):
   class Meta:
      model = financas
      fields = ['status','parcela', 'data_pagamento', 'banco', 'arquivo']
      widgets = {
            'status': forms.HiddenInput(),
            'parcela': forms.TextInput(attrs={'readonly': 'readonly'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date',}),
            'banco': forms.TextInput(attrs={'type': 'text'}),
            'arquivo': forms.FileInput(attrs={'type': 'file'}),
            }