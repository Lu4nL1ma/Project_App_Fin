from django.test import TestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import sqlite3

# conection = sqlite3.connect('C:\\Users\\corpl\\OneDrive\\10_Django\\fin_tech\\db.sqlite3')

# cursor = conection.cursor()

# # fim = np.arange(1058,1077+1,1)

# # for i in fim:

# #     delete_query = f'DELETE FROM financas_online_financas WHERE id={i}'

# #     #delete_query = f'DROP TABLE IF EXISTS {i}'

# #     cursor.execute(delete_query)

# # cursor.execute("SELECT * FROM minha_tabela")


# # results = cursor.fetchall()

# # for row in results:
# #     print(row)

# conection.commit()

# conection.close()

texto = '040.012.042-90'

texto = texto.strip().replace('.', '').replace('-', '')

print(texto)