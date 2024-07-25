import pymssql
import pandas as pd

conn = pymssql.connect(
    host=r'fdb1033.awardspace.net:3306', #pro.freedb.tech:3306',
    user=r'4469908_user',#'#DummyUsername1\user',
    password=r'Mastr',
    database='4469908_user'
)

print('Connect')
cursor = conn.cursor(as_dict=True)
print('Cursor')
cursor.execute('Select top 4 location_id, description from t_location with (nolock)')
print('Fetch')
data = cursor.fetchall()
data_df = pd.DataFrame(data)
print(data_df.head())

cursor.close()

