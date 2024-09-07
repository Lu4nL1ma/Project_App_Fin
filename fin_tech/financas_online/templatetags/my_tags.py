from django import template

register = template.Library()

@register.filter
def formata_cpf(value):
    # Lógica para formatar o CPF
    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"