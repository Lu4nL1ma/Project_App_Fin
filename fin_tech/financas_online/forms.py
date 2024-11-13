from financas_online.models import customers, financas
from financas_online.models import customers, financas, cursos, turmas_formatec
from django.forms import ModelForm
from django import forms
from datetime import datetime

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
      
class parcelaform(ModelForm):
   class Meta:
      model = financas
      fields = ['id_ori', 'parcela', 'cliente', 'valor', 'curso', 'turma', 'vencimento']
      parcela = [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)]
      widgets = {
            'id_ori': forms.TextInput(attrs={'type': 'hidden',}),
            'cliente': forms.TextInput(attrs={'type': 'hidden',}),
            'curso' : forms.Select(choices=[]),
            'turma' : forms.Select(choices=[]),
            'parcela' : forms.Select(choices=parcela),
            'valor': forms.TextInput(attrs={'type': 'text',}),
            'vencimento': forms.DateInput(attrs={'type': 'date',}),
        }      
      
class updtparcelaform(ModelForm):
   class Meta:
      model = financas
      fields = ['status', 'parcela','data_pagamento', 'tipo_pagamento', 'banco', 'arquivo']
      pay = [('Pix','Pix'), ('Dinheiro', 'Dinheiro'), ('Cartão de Crédito', 'Cartão de Crédito'), ('Cartão de Débito', 'Cartão de Dédito')]
      labels = {'parcela':'Nº da Parcela', 'data_pagamento':'Data do Pagamento', 'arquivo': 'Comprovante', 'tipo_pagamento': 'Tipo de Pagamento'}
      widgets = {
            'status': forms.HiddenInput(),
            'parcela': forms.TextInput(attrs={'readonly': 'readonly'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date',}),
            'tipo_pagamento' : forms.Select(choices=pay),
            'banco': forms.TextInput(attrs={'type': 'text'}),
            'arquivo': forms.FileInput(attrs={'type': 'file'}),
            }
      
class form_dash(forms.Form):

   ano = forms.ChoiceField(choices=[])
     
   mes = forms.ChoiceField(
        choices=[
            (1, 'Janeiro'),
            (2, 'Fevereiro'),
            (3, 'Março'),
            (4, 'Maio'),
            (6, 'Junho'),
            (7, 'Julho'),
            (8, 'Agosto'),
            (9, 'Setembro'),
            (10, 'Outubro'),
            (11, 'Novembro'),
            (12, 'Dezembro'),
        ]
    )
   

   curso = forms.ChoiceField(choices=[])


   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ano_atual = datetime.now().year
        anos = [(ano, str(ano)) for ano in range(2020, ano_atual + 7)]
        self.fields['ano'].choices = anos
        self.fields['curso'].choices = cursos.objects.all().values_list('curso','curso')

      