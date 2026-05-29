import sqlite3
import pandas as pd

df = pd.read_csv('bogota_temps.csv')

print(df.head())

try:
    with sqlite3.connect("historic_temps.db") as conn:
        print("Database created and connected successfully.")

        df.to_sql(name = 'bogota', con=conn, if_exists='replace', index=False)

except sqlite3.Error as e:
    print(f"Error ocurred: {e}")