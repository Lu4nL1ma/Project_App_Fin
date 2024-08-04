
from django.shortcuts import get_object_or_404, render, redirect
from financas_online.models import cursos, customers, turmas_formatec, financas
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q



# Create your views here.

app_name = 'financas_online'


def index(request):
 
 if request.method == 'POST':
    
     ids = request.POST.getlist('ids_slct')

     del_cliente = customers.objects.filter(id__in=ids)

     del_cliente.delete()

     clientes = customers.objects.all().order_by('id')

     context = {'customer': clientes}
     
     return render(request, 'index.html', context)
 
 else:
   
   clientes = customers.objects.all().order_by('id')

   context = {'customer': clientes}
 
   return render(request, 'index.html', context)


def buscar(request):
 
   buscar_valor = request.GET.get('q', '').strip()
 
   if buscar_valor == '':
      return redirect('index')
 
   else:
    
    clientes = customers.objects.filter(Q(nome__icontains=buscar_valor) | Q(id__icontains=buscar_valor)).order_by('id')

    context = {'customer': clientes}
 
    return render(request, 'index.html', context)
 

def inserir(request):

   turmas = turmas_formatec.objects.all().order_by('id')

   course = cursos.objects.all().order_by('id')

   dados = {'course': course,
            'turmas': turmas}

   if request.method == 'POST':
     nome = request.POST['nome']
     cpf = request.POST['cpf']
     telefone = request.POST['tele']
     nasicmento = request.POST['nasc']

     add_cliente = customers(nome=nome, cpf=cpf, telefone=telefone, nascimento=nasicmento)

     add_cliente.save()
   
   return render(request, 'form_inse.html', dados)


def apagar(request):
     
   if request.method == 'POST':
    
     id = request.POST['ids_slct']

     del_cliente = customers.objects.filter(id=id)

     del_cliente.delete()
     
     return render(request, 'form_del.html')
   
   
   

def customer(request, c_id):

   if request.method == 'GET':
   
      id_cliente = customers.objects.get(pk=c_id)

      fin = financas.objects.filter(id_ori=c_id)

      context = {'c': id_cliente,
                'fin': fin}
      return render(request, 'customer.html', context)
   

#condicional do método post
   elif request.method == 'POST':
     
     ids = request.POST.getlist('ids_slct')

     del_cliente = customers.objects.filter(id__in=ids)

     del_cliente.delete()

     id_ori = request.POST['id_ori']
     nome = request.POST['nome_cli']
     parcelas = request.POST['parc']
     valor = request.POST['vlo']
     vencimento = request.POST['vnc']
    
     if int(parcelas) == 1:
      
      add_financeiro = financas(cliente=nome, parcela=parcelas, valor=valor, data=vencimento, id_ori=id_ori)
      add_financeiro.save()
      
      return render(request, 'customer.html', context) 

#condicional de repetição das parcelas > 1     
     elif int(parcelas) > 1:
      
       contador = 0
       end = int(parcelas)

       while contador < end:
         data_edit = datetime.strptime(vencimento,'%Y-%m-%d') + relativedelta(months=contador)
         parcela_edit = f'0{contador+1}/0{end}'
         add_financeiro = financas(cliente=nome, parcela=parcela_edit, valor=valor, data=data_edit, id_ori=id_ori)
         add_financeiro.save()
         contador += 1
     return render(request, 'customer.html', context)
   


#view do forms inserir parcelas
def form(request, c_id):

  if request.method == 'GET':
     
     id_clientes = customers.objects.get(pk=c_id)

     context = {'c': id_clientes}
     
     return render(request, 'forms.html', context)

  
  



   
   


   



   
    
    