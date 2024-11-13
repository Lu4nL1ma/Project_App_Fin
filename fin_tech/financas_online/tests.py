def formata_reais(valor):
    """Formata um valor numérico para o padrão brasileiro de reais."""
    return locale.currency(valor, grouping=True)

valor = 10000

p = formata_reais(valor)

print(p)