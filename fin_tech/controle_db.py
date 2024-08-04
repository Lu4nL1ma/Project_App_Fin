import sqlite3
import numpy as np



conection = sqlite3.connect('fin_tech\\db.sqlite3')

cursor = conection.cursor()

fim = ["django_session"]


for i in fim:

    #delete_query = f'DELETE FROM auth_permission WHERE {i}'

    delete_query = f'DROP TABLE IF EXISTS {i}'

    cursor.execute(delete_query)

#delete_query = 'DROP TABLE IF EXISTS financas_online_financeiro'

#cursor.execute(delete_query)

conection.commit()

conection.close()

