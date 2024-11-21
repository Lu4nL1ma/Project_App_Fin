import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import locale

# Definir o locale para português do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def enviar_email(destinatario, assunto, corpo):
    """Envia um email para o destinatário especificado.

    Args:
        destinatario (str): Endereço de e-mail do destinatário.
        assunto (str): Assunto do email.
        corpo (str): Corpo do email.
    """

    # Configurações do seu email
    sender_email = "luanlima.corp@gmail.com"
    password = 'ndwu zglz uszl cgze'

    # Cria a mensagem
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = destinatario
    message["Subject"] = assunto

    # Corpo da mensagem em texto simples
    message.attach(MIMEText(corpo, "plain"))

    # Conecta ao servidor SMTP e envia a mensagem
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, destinatario, message.as_string())
# Data atual.
hoje = datetime.date.today()

dia = hoje.strftime("%A")

# variaveis para envio
pessoa = ['Luan','Evelym']
destinatarios = ["2019luangl@gmail.com","evelymsantos805@gmail.com"]
c = 0

if dia != "Sábado" and dia != "Domingo":
    if dia == "segunda-feira":

        # Envia um email para cada destinatário
        for destinatario in destinatarios:
            c
            assunto = f"Que sua semana seja produtiva querido(a) {pessoa[c]}!"
            corpo = f"Olá, querido(a) {pessoa[c]}, venho nesta {dia} lembrar que você é muito especial e estou passando para lhe desejar uma ótima semana, acredite em si mesmo, pois você é muito capaz, bem além do que você mesmo pode imaginar! S2"
            enviar_email(destinatario, assunto, corpo)
            c = c+1
    elif dia == "sexta-feira":

        # Envia um email para cada destinatário
        for destinatario in destinatarios:
            c
            assunto = f"Descanse querido(a) {pessoa[c]}!"
            corpo = f"Olá, querido(a) {pessoa[c]}, venho nesta {dia} lembrar que você merece um descanso da correria que foi esta semana, aproveite o final de semana! S2"
            enviar_email(destinatario, assunto, corpo)
            c = c+1
