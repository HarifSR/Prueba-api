# app/db.py
import pyodbc
import os

def get_db_connection():
    """Crea y retorna una conexión a la base de datos."""
    # Lee las variables de entorno configuradas en tu servidor (Render/Azure)
    server = os.environ.get('DB_SERVER', 'svr-sql-ctezo.southcentralus.cloudapp.azure.com')
    database = os.environ.get('DB_DATABASE', 'db_DesaWebDevUMG')
    username = os.environ.get('DB_USERNAME', 'usr_DesaWebDevUMG')
    password = os.environ.get('DB_PASSWORD', '!ngGuast@360')
    
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    return pyodbc.connect(connection_string)