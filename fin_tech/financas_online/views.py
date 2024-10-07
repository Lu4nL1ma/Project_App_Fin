
from django.shortcuts import get_object_or_404, render, redirect
from financas_online.models import cursos, customers, turmas_formatec, financas
from django.contrib.auth.decorators import login_required
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
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

   if request.method == 'POST':
     nome = request.POST['nome']
     cpf = request.POST['cpf']
     telefone = request.POST['tele']
     nasicmento = request.POST['nasc']

     add_cliente = customers(nome=nome, cpf=cpf, telefone=telefone, nascimento=nasicmento)

     add_cliente.save()

     return redirect('index')
   
   else:
     
     turmas = turmas_formatec.objects.all().order_by('id')

     course = cursos.objects.all().order_by('id')

     dados = {'course': course,
            'turmas': turmas}
     
     return render(request, 'form_inse.html', dados)

#view de controle da página de usuários
def customer(request, c_id):
   id_cliente = customers.objects.get(pk=c_id)
   fin = financas.objects.filter(id_ori=c_id)
   context = {'c': id_cliente,'fin': fin}
   
   if request.method == 'GET':
      
      return render(request, 'customer.html', context)
#condicional do método post
   elif request.method == 'POST':
     
     if 'b_d_p' in request.POST:
       
       dele = request.POST.getlist('ids_slct_fin')
       del_cliente = financas.objects.filter(id__in=dele)
       del_cliente.delete()
       return render(request, 'customer.html', context)
     
     elif 'i_p' in request.POST:       
      id_ori = request.POST['id_ori']
      nome = request.POST['nome_cli']
      curs = request.POST['curs_p']
      turms = request.POST['turms']
      parcelas = request.POST['parcs']
      valor = request.POST['vlo']
      vencimento = request.POST['vnc']
      
      if int(parcelas) == 1:
         parcs = f'0{parcelas}/0{parcelas}'
         add_financeiro = financas(cliente=nome, parcela=parcs, valor=valor, vencimento=vencimento, id_ori=id_ori, curso=curs, turma=turms)
         add_financeiro.save()
         return render(request, 'customer.html', context) 

#condicional de repetição das parcelas > 1     
      elif int(parcelas) > 1:
      
       contador = 0
       end = int(parcelas)

       while contador < end:
         data_edit = datetime.strptime(vencimento,'%Y-%m-%d') + relativedelta(months=contador)
         parcela_edit = f'0{contador+1}/0{end}'
         add_financeiro = financas(cliente=nome, parcela=parcela_edit, valor=valor, vencimento=data_edit, id_ori=id_ori, curso=curs, turma=turms)
         add_financeiro.save()
         contador += 1
      return render(request, 'customer.html', context)

#atualização dos dados do cliente    
     elif 'up_date_cli' in request.POST:
       
       id = request.POST['up_id_cli']
       nome = request.POST['up_nom_cli']
       cpf = request.POST['up_cpf_cli']
       telefone = request.POST['up_tel_cli']
       nascimento = request.POST['up_nsc_cli']
       date_edits = datetime.strptime(nascimento,'%d/%m/%Y')

      
       filtro = customers.objects.filter(pk=id) 
       filtro.update(nome=nome, cpf=cpf, telefone=telefone, nascimento=date_edits)
      #  filtro.save()
       
       return render(request, 'customer.html', context)
 
     elif 'upd_p' in request.POST:
        
        id = request.POST['id_up_f']
        pagamento = request.POST['up_pg_cli']
        banco = request.POST['up_banco']
        comprovante = request.POST['up_file']
        filtro = financas.objects.filter(pk=id) 
        filtro.update(data_pagamento=pagamento, banco=banco, arquivo=comprovante)
   
#view do forms inserir parcelas
def form(request, c_id):

  if request.method == 'GET':
     
     id_clientes = customers.objects.get(pk=c_id)

     parcelas = np.arange(1,6+1,1)

     curs = cursos.objects.all()

     turms = turmas_formatec.objects.all()

     context = {'c': id_clientes, 'parcs':parcelas, 'curs': curs, 'turms': turms}
     
     return render(request, 'forms.html', context)

def login(request):
     
     return render(request, 'login.html')

def updatefin(request,c_id, f_id):
   id_cliente = customers.objects.get(pk=c_id)
   fin = financas.objects.get(id=f_id)
   context = {'c': id_cliente,'f': fin}
   return render(request, 'updatefin.html', context)

def update_cliente(request, c_id):
     
     id_cliente = customers.objects.get(pk=c_id)
     context = {'c': id_cliente}
    
     return render(request,'updatecli.html', context)


   
   


   



   
    
    