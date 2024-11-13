from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from financas_online.models import cursos, customers, turmas_formatec, financas
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import customerform, parcelaform, updtparcelaform, form_dash
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from PIL import Image
from django.conf import settings
from urllib.parse import quote
from fpdf import FPDF
from pathlib import Path
from num2words import num2words
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import locale
import os
import io


# Create your views here.
app_name = 'financas_online'

#diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

#definir local global
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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

     for d in del_fin:
        
        filed = d.arquivo

        try:
            caminho = os.path.join(BASE_DIR, f'media\\comprovantes\\{filed}')

            os.remove(caminho)

            del_fin.delete()
        
        except:
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
         msg = f'Olá, {f_nome} {l_nome}, somos da Formatec, segue as informações do débito abaixo:'
         link_wpp = f'https://web.whatsapp.com/send/?phone=55{numero}&text={quote(msg)}%0A%0A'
      for f in fin:
         if f.valor != "":
            
            valor_edit = int(f.valor)

            context = {'c': id_cliente,'fin': fin, 'url': url_arquivo, 'link_wpp': link_wpp, 'valor_edit': valor_edit}
         else:
            context = {'c': id_cliente,'fin': fin, 'url': url_arquivo, 'link_wpp': link_wpp}    

      return render(request, 'customer.html', context)

#condicional do método post
   elif request.method == 'POST':
      
       dele = request.POST.getlist('ids_slct_fin')

       fin = financas.objects.filter(id__in=dele)

       for f in fin:
         
         filed = f.arquivo

         print(f'DADOOOO: {filed}')

         try:
            caminho = os.path.join(BASE_DIR, f'media\\comprovantes\\{filed}')

            os.remove(caminho)

            del_cliente = financas.objects.filter(id__in=dele)
       
            del_cliente.delete()
         
         except:

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

        valor = int(valor)
        
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

        tipo_pagamento = form_updt.cleaned_data['tipo_pagamento']

        banco = form_updt.cleaned_data['banco']

        arquivo = form_updt.cleaned_data['arquivo']

        banco = banco.title()

      #edições nos dados
        status = 'Recebido'

        file_date = data_pagamento.strftime('%d_%m_%Y')

        file_name = f'ID-{f_id}_PG-{file_date}.png'
        
        if arquivo is not None:
           
         img = Image.open(arquivo)

         path = os.path.join(settings.BASE_DIR, f'media/comprovantes/{file_name}')

         img = img.save(path)
         
         financas.objects.filter(id=f_id).update(status=status, parcela=parcela, data_pagamento=data_pagamento, tipo_pagamento=tipo_pagamento, banco=banco, arquivo=file_name)

        else:
           financas.objects.filter(id=f_id).update(status=status, parcela=parcela, data_pagamento=data_pagamento, tipo_pagamento=tipo_pagamento, banco=banco, arquivo="")
     
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

@login_required
def download_recibo(request, c_id, f_id):

   #filtrar dados

   dados_financeiros = financas.objects.filter(pk=f_id)

   dados_clientes = customers.objects.filter(pk=c_id)

   # Cria um objeto PDF
   pdf = FPDF()

   # Adiciona uma página
   pdf.add_page()

   # logo
   caminho = caminho = os.path.join(BASE_DIR, 'media')
   pdf.image(f'{caminho}/files_clients/formatec.png', x=11.5, y=10, w=30, h=20)

   # Define a fonte
   pdf.set_font("Arial", "B", size=10)
   
   #cells do nome e cnpj
   pdf.set_x(22)
   pdf.set_y(28)
   pdf.cell(30, 10, ' NOGUEIRA LTDA', 0, 1,)

   pdf.set_x(30)
   pdf.set_y(32)
   pdf.cell(30, 10, '36.194.235/0001-09', 0, 1,)

   #fonte do titulo
   pdf.set_font("Arial", "B", size=18)

   # Título centralizado
   pdf.set_x(10)  # Volta para o início da linha
   pdf.set_y(10)
   pdf.cell(200, 10, 'RECIBO', 0, 1, 'C')

   data = timezone.now().date()
   data = data.strftime('%d de %B de %Y')

   pdf.set_font("Arial", size=16)
   pdf.set_x(70)
   pdf.set_y(100)

   for f in dados_financeiros:
      cliente = f.cliente
      valor = f.valor
      valor_extens = num2words(valor, lang='pt_BR')
      parcela = f.parcela
      vencimento = f.vencimento
      vencimento = vencimento.strftime('%d/%m/%Y')
      curso = f.curso
      turma = f.turma

      for c in dados_clientes:
         cpf = c.cpf
         pdf.set_x(10)
         pdf.set_y(80)
         pdf.multi_cell(190, 10,  f'   Declaro ter recebido de {cliente} inscrito(a) no CPF de nº. {f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"}, nesta data presente a quantia de R$ {valor},00 ({valor_extens} reais), referente a parcela {parcela} com vencimento em {vencimento} do curso de {curso} na {turma}.', 1)

   pdf.set_x(10)
   pdf.set_y(150)
   pdf.cell(200, 5,  'E para maior clareza, firmo o presente.', 0, 1, 'L')

   pdf.set_x(10)
   pdf.set_y(175)
   pdf.cell(200, 5,  f'Belém-PA, {data}.', 0, 1, 'C')

   pdf.set_x(10)
   pdf.set_y(222)
   pdf.cell(200, 5, '________________________________', 0, 1, 'C')

   pdf.set_font("Arial", size=16)

   pdf.set_x(10)
   pdf.set_y(232)
   pdf.cell(200, 5, 'Assinatura', 0, 1, 'C')

   # Salvar o conteúdo do PDF em memória (usando BytesIO)
   
   buffer = io.BytesIO()
   
   pdf_output = pdf.output(dest='S').encode('latin1') 
   
   buffer = io.BytesIO(pdf_output)
  
   buffer.seek(0)

    # Criar a resposta HTTP com o conteúdo do PDF
   response = HttpResponse(buffer, content_type='application/pdf')

    # Definir cabeçalho para visualização no navegador ou para download
   response['Content-Disposition'] = f'inline; filename="recibo_id{f_id}.pdf"'  # Para visualização
   # response['Content-Disposition'] = 'attachment; filename="meu_arquivo.pdf"'  # Para download
   
   return response

@login_required
def dashboard_financeiro(request):
      
      if "filter" in request.method == 'POST':
         
         #valores dos filtros

         ano = request.GET.get('ano')

         mes = request.GET.get('mes')

         curso = request.GET.get('curso')
         
         #dados
         fins = financas.objects.values_list('status', 'cliente', 'curso', 'valor', 'vencimento')
         df = pd.DataFrame(fins, columns=['Status', 'Cliente', 'Curso','Valor', 'Vencimento'])

         # # Criando os dados para o gráfico

         df['Valor'] = df['Valor'].astype(int)
         df['Curso'] = df['Curso'].astype(str)
         df['Vencimento'] = pd.to_datetime(df['Vencimento'])
         df['Ano'] = df['Vencimento'].dt.year
         df['Mês'] = df['Vencimento'].dt.month

         #filtrando valores
         df = df[df['Ano'] == ano]
         df = df[df['Mês'] == mes]

      else:
         #dados
         fins = financas.objects.values_list('status', 'cliente', 'curso', 'valor', 'vencimento')
         df = pd.DataFrame(fins, columns=['Status', 'Cliente', 'Curso','Valor', 'Vencimento'])

         # # Criando os dados para o gráfico

         df['Valor'] = df['Valor'].astype(int)
         df['Curso'] = df['Curso'].astype(str)
      
      # print(df)

      x = df['Curso']
      y = df['Valor']

      #somas para o dash

      faturado = df[df['Status'] == 'Recebido']['Valor'].sum()

      receber = df[df['Status'] == 'A receber']['Valor'].sum()

      vencido = df[df['Status'] == 'Vencido']['Valor'].sum()

      unicos = df['Cliente'].nunique()

      month = list(range(1, 13))

      #cores
      cor_interna = '#F0FFF0'
      cor_externa = '#F0FFFF'

      fig = go.Figure(go.Bar(
      x=df['Valor'],
      y=df['Curso'],
      width=0.3,
      orientation='h',
      marker=dict(color='#4682B4')
      ))


      fig.update_layout(plot_bgcolor=cor_interna, paper_bgcolor=cor_externa, height=400, width=460,title_text='Faturamento Por Curso', title_x=0.5, xaxis_title='Demanda', yaxis_title='Curso', font=dict(family='Arial', color='#000000', size=16))


      # Convertendo o gráfico para HTML
      div = fig.to_html(full_html=False)

      # Criando um DataFrame com dados fictícios
      df = pd.DataFrame({'Mês': month,
                        'Vendas': month})

      # Criando o gráfico de linha
      fig_three = go.Figure(data=go.Scatter(x=df['Mês'], y=df['Vendas'], mode='lines+markers'))

      # Personalizando o gráfico
      fig_three.update_layout(
         plot_bgcolor=cor_interna, paper_bgcolor=cor_externa,
         title="Análise de Crescimento Mensal",
         xaxis_title="Mês",
         yaxis_title="Faturamento",
         hovermode="x unified",
         height=400, width=460,
         title_x=0.5,
         font=dict(family='Arial', color='#000000', size=16)
         
      )

      div_three = fig_three.to_html(full_html=False)

      context = {'div':div, 'div_three': div_three, 'faturado': faturado, 'receber': receber, 'vencido': vencido, 'unicos': unicos, 'form': form_dash}
      
      return render(request, 'dashboard_fin.html', context)



   
   


   



   
    
    