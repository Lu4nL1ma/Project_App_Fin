from django.shortcuts import get_object_or_404, render, redirect
from financas_online.models import cursos, customers, turmas_formatec, financas
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import customerform, parcelaform, CustomLoginForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

# Create your views here.
app_name = 'financas_online'

#view de home e apagar clientes
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
def buscar(request):
 
   buscar_valor = request.GET.get('q', '').strip()
 
   if buscar_valor == '':
      return redirect('index')
 
   else:
    
    clientes = customers.objects.filter(Q(nome__icontains=buscar_valor) | Q(id__icontains=buscar_valor)).order_by('id')

    context = {'customer': clientes}
 
    return render(request, 'index.html', context)
 
#view de inserir clientes
def inserir(request):

   if request.method == 'GET':

      form = customerform()

      dados = {'form': form}
     
      return render(request, 'form_inse.html', dados)
   
   if request.method == 'POST':
      
      form = customerform(request.POST)
      
      if form.is_valid():
        
        form.save()
      
      return redirect('index')

#view de controle da página de usuários
def customer(request, c_id):
   
   if request.method == 'GET':

      id_cliente = customers.objects.get(pk=c_id)
      
      fin = financas.objects.filter(id_ori=c_id)
      
      context = {'c': id_cliente,'fin': fin}
      
      return render(request, 'customer.html', context)

#condicional do método post
   elif request.method == 'POST':
      
       dele = request.POST.getlist('ids_slct_fin')
       
       del_cliente = financas.objects.filter(id__in=dele)
       
       del_cliente.delete()
       
       return render(request, 'customer.html', context)
       
#view do forms inserir parcelas
def form(request, c_id):

  if request.method == 'GET':
     
     c = customers.objects.get(pk=c_id)

     form_parc = parcelaform(initial={'id_ori': c_id, 'cliente': c.nome})

     context = {'c': c, 'form_parc': form_parc}
     
     return render(request, 'forms.html', context)
  
  elif request.method == 'POST':
     
     form_parc = parcelaform(request.POST)
     
     if form_parc.is_valid():
        
        form_parc.save()
     
     return redirect(reverse('cliente', args=[c_id]))

def login(request):
   
   form = AuthenticationForm(request)
   
   if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
         user = form.get_user()
         auth.login(request, user)
         return redirect('index')
        else:
            form = CustomLoginForm()
            return render(request, 'login.html', {'form':form})
   else:
      return render(request, 'login.html', {'form':form})
            

     


def updatefin(request,c_id, f_id):
   id_cliente = customers.objects.get(pk=c_id)
   fin = financas.objects.get(id=f_id)
   context = {'c': id_cliente,'f': fin}
   return render(request, 'updatefin.html', context)

def update_cliente(request, c_id):
     
     id_cliente = customers.objects.get(pk=c_id)
     context = {'c': id_cliente}
    
     return render(request,'updatecli.html', context)
     
    


   
   


   



   
    
    