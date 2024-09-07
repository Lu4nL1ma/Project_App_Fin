import sqlite3
import numpy as np



conection = sqlite3.connect('fin_tech\\db.sqlite3')


cursor = conection.cursor()

#fim = ["django_session"]

fim = np.arange(1058,1077+1,1)

for i in fim:

    delete_query = f'DELETE FROM financas_online_financas WHERE id={i}'

    #delete_query = f'DROP TABLE IF EXISTS {i}'

    cursor.execute(delete_query)

conection.commit()

conection.close()

