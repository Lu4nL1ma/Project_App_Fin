from django.test import TestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your tests here.

mes_comercial = 1

vencimento = '2024-07-31'

data_edit = datetime.strptime(vencimento,"%Y-%m-%d") + relativedelta(months=mes_comercial)

print(data_edit)