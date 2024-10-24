import json
import sqlite3

# Function to initialize the database and create the table if it doesn't exist
def init_db():
    conn = sqlite3.connect("eventos.db")
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            IdGeo INTEGER,
            TipoEvento INTEGER,
            Longitud REAL,
            Latitud REAL,
            Fecha REAL
        )
    ''')
    conn.commit()
    conn.close()

# Function to load data from JSON into the database
def cargar_json_a_db(archivo_json):
    conn = sqlite3.connect("eventos.db")
    cursor = conn.cursor()

    # Parse JSON data
    with open(archivo_json, 'r') as f:
        datos = json.load(f)['rows']
    
    for row in datos:
        # Insert the event directly into the database
        cursor.execute('''
            INSERT INTO eventos (IdGeo, TipoEvento, Longitud, Latitud, Fecha)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['IdGeo'], row['TipoEvento'], row['Longitud'], row['Latitud'], row['Fecha']))
    
    conn.commit()
    conn.close()
    print(f"Datos del archivo {archivo_json} cargados con éxito en la base de datos.")

# Inicializa la base de datos y la tabla
init_db()

# Archivo JSON de entrada
archivo_json = 'ficheros/eventosMadrid_Sep_2024_emisiones_RANDOM.json'  

# Llamar a la función para cargar el archivo en la base de datos
cargar_json_a_db(archivo_json)
