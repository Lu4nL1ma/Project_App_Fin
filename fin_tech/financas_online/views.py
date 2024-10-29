from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from financas_online.models import cursos, customers, turmas_formatec, financas
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import customerform, parcelaform, updtparcelaform
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from PIL import Image
from django.conf import settings
from urllib.parse import quote
import numpy as np
import os


# Create your views here.
app_name = 'financas_online'

#view de login
def login(request):
   
   form = AuthenticationForm(request)
   
   if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
         user = form.get_user()
         auth.login(request, user)
         return redirect('index')
        else:
            return render(request, 'login.html', {'form':form})
   else:
      return render(request, 'login.html', {'form':form})

def logout(request):
   auth.logout(request)
   return redirect('login')

#view de home e apagar clientes
@login_required
def index(request):
 
 if request.method == 'POST':
    
     ids = request.POST.getlist('ids_slct')

     del_cliente = customers.objects.filter(id__in=ids)

     del_cliente.delete()

     del_fin = financas.objects.filter(id_ori__in=ids)

     del_fin.delete()

     clientes = customers.objects.all().order_by('id')

     context = {'customer': clientes}
     
     return render(request, 'index.html', context)
 
 else:
   
   clientes = customers.objects.all().order_by('id')

   context = {'customer': clientes}
 
   return render(request, 'index.html', context)

#view de buscar registros
@login_required
def buscar(request):
 
   buscar_valor = request.GET.get('q', '').strip()
 
   if buscar_valor == '':
      return redirect('index')
 
   else:
    
    clientes = customers.objects.filter(Q(nome__icontains=buscar_valor) | Q(id__icontains=buscar_valor)).order_by('id')

    context = {'customer': clientes}
 
    return render(request, 'index.html', context)
 
#view de inserir clientes
@login_required
def inserir(request):

   if request.method == 'GET':

      form = customerform()

      dados = {'form': form}
     
      return render(request, 'form_inse.html', dados)
   
   if request.method == 'POST':
      
      form = customerform(request.POST)
      
      if form.is_valid():
        
        nome = form.cleaned_data['nome']

        cpf = form.cleaned_data['cpf']
        
        telefone = form.cleaned_data['telefone']

        nascimento = form.cleaned_data['nascimento']

        #edit dados do forms

        nome = nome.title().strip()

        telefone = telefone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')

        cpf = cpf.strip().replace('.', '').replace('-', '')

        cliente = customers.objects.create(nome=nome, cpf=cpf, telefone=telefone, nascimento=nascimento)
        
        cliente.save()
      
      return redirect('index')
   
#view de customer.
@login_required
def customer(request, c_id):
   
   if request.method == 'GET':

      financas.objects.filter(status="A receber", vencimento__lt=timezone.now().date()).update(status="Vencido")

      id_cliente = customers.objects.get(pk=c_id)

      list = customers.objects.filter(pk=c_id)
      
      fin = financas.objects.filter(id_ori=c_id)

      url_arquivo = os.path.join(settings.MEDIA_URL, 'media/comprovantes/')

      for l in list:
         f_nome = l.nome.split()[0]
         l_nome = l.nome.split()[-1]
         numero = l.telefone
         msg = f'Olá, {f_nome} {l_nome}, somos da Formatec, e você têm o débito abaixo pendente:'
         link_wpp = f'https://web.whatsapp.com/send/?phone=55{numero}&text={quote(msg)}%0A'

      context = {'c': id_cliente,'fin': fin, 'url': url_arquivo, 'link_wpp': link_wpp}
      
      return render(request, 'customer.html', context)

#condicional do método post
   elif request.method == 'POST':
      
       dele = request.POST.getlist('ids_slct_fin')
       
       del_cliente = financas.objects.filter(id__in=dele)
       
       del_cliente.delete()
       
       return redirect(reverse('cliente', args=[c_id]))
       
#view do forms inserir parcelas
@login_required
def form(request, c_id):

  if request.method == 'GET':
     
     c = customers.objects.get(pk=c_id)

     form_parc = parcelaform(initial={'id_ori': c_id, 'cliente': c.nome})

     context = {'c': c, 'form_parc': form_parc}
     
     return render(request, 'forms.html', context)
  
  elif request.method == 'POST':
     
     form_parc = parcelaform(request.POST)
     
     if form_parc.is_valid():
        
        #pegar dados do formulário
        
        id_ori = form_parc.cleaned_data['id_ori']

        cliente = form_parc.cleaned_data['cliente']
        
        parcela = form_parc.cleaned_data['parcela']

        valor = form_parc.cleaned_data['valor']
        
        curso = form_parc.cleaned_data['curso']

        turma = form_parc.cleaned_data['turma']

        vencimento = form_parc.cleaned_data['vencimento']
        
        #TRATAR DADOS DO FORMULÁRIO
        
        condicional = int(parcela)

        date = str(vencimento)
        
        #CONDICIONAL DE UMA INCLUSÃO NO BANCO DE DADOS
        
        if condicional == 1:
           
           parcela_editada = f'0{parcela}/0{parcela}'

           parcelas = financas.objects.create(id_ori=id_ori, cliente=cliente, parcela=parcela_editada, valor=valor, curso=curso, turma=turma, vencimento=vencimento)
        
           parcelas.save()
           
           return redirect(reverse('cliente', args=[c_id]))
       

        #CONDICIONAL DE UMA INCLUSÃO DE REPETIÇAÕ DE PARCELAS
        
        elif condicional != 1:
           
           contador = 1

           meses = 0
        
           while contador < condicional+1:
              
              data_editada = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=meses)
         
              parcela_editada = f'0{contador}/0{parcela}'

              parcelas = financas.objects.create(id_ori=id_ori, cliente=cliente, parcela=parcela_editada, valor=valor, curso=curso, turma=turma, vencimento=data_editada)
        
              parcelas.save()

              contador = contador + 1

              meses = meses + 1
      
        return redirect(reverse('cliente', args=[c_id]))
      
#atualizar financeiro            
@login_required
def updatefin(request,c_id, f_id):
   
   if request.method == "GET":
      c = customers.objects.get(pk=c_id)
      f = financas.objects.get(id=f_id)
      form_updt = updtparcelaform(initial={'parcela': f.parcela})
      context = {'c': c,'f': f, 'form_updt': form_updt}
      return render(request, 'updatefin.html', context)
   
   elif request.method == "POST":
      
      form_updt = updtparcelaform(request.POST, request.FILES)

      print(request.FILES)
      
      if form_updt.is_valid():
        
        #pegar dados do formulário

        parcela = form_updt.cleaned_data['parcela']
        
        status = form_updt.cleaned_data['status']
        
        data_pagamento = form_updt.cleaned_data['data_pagamento']

        banco = form_updt.cleaned_data['banco']

        arquivo = form_updt.cleaned_data['arquivo']

      #edições nos dados
        status = 'Recebido'

        file_date = data_pagamento.strftime('%d_%m_%Y')

        file_name = f'ID{f_id} - PG{file_date}'
        
        if arquivo is not None:
           
         img = Image.open(arquivo)

         path = os.path.join(settings.BASE_DIR, f'media/comprovantes/{file_name}.png')

         img = img.save(path)

      financas.objects.filter(id=f_id).update(status=status, parcela=parcela, data_pagamento=data_pagamento, banco=banco, arquivo=file_name)
     
   return redirect(reverse('cliente', args=[c_id]))

#atualizar cliente
@login_required
def update_cliente(request, c_id):
     
     id_cliente = customers.objects.get(pk=c_id)
     context = {'c': id_cliente}
    
     return render(request,'updatecli.html', context)
 

 #view de inserir curso.

#inserir curso
@login_required
def curso(request):

   if request.method == 'POST':
         
         curso = request.POST.get('curso')

         curso = curso.title()

         inserir = cursos(curso=curso)

         inserir.save()
         
         return redirect('index')
   else:
      return render(request, 'inserir_curso.html')

#inserir turma
@login_required
def turma(request):

   if request.method == 'POST':
         
         turma = request.POST.get('turma')

         turma = turma.title()

         inserir = turmas_formatec(turmas_formatec=turma)

         inserir.save()
         
         return redirect('index')
   else:
      return render(request, 'inserir_turma.html')    

   





   
   


   



   
    
    