import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

# variaveis para envio
pessoa = ['Luan','Evelym', 'Yas']
destinatarios = ["2019luangl@gmail.com","evelymsantos805@gmail.com", "yasminkristine123@gmail.com"]
c = 0

# Assunto e corpo do email (pode ser personalizado para cada destinatário)
assunto = "Assunto do email"
corpo = "Olá, este é um email personalizado para você!"

# Envia um email para cada destinatário
for destinatario in destinatarios:
    c
    assunto = f"Saudação carinhosa para você {pessoa[c]}!"
    corpo = f"Olá, querido(a) {pessoa[c]}, lembrando que você é muito especial e estou passando para lhe desejar um ótimo dia! S2"
    enviar_email(destinatario, assunto, corpo)
    c = c+1