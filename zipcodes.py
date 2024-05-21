import pandas as pd
from sqlalchemy import create_engine

# Setting up a database
hostname = "127.0.0.1"
uname = "root"
pwd = ""
dbname = "zipcodes"

# Set up an engine and connect to the database system.
engine = create_engine(f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}")

# Using a pandas dataframe to read the CSV file.
csv_file_path = r"C:\Users\abiyu\Downloads\zip_code_database.csv"
tables = pd.read_csv(csv_file_path)

# Transfer the dataframe to the mySQL database.
connection = engine.connect()
tables.to_sql('zipcodes', con=engine, if_exists='replace', index=False)
connection.close()
print(tables)
