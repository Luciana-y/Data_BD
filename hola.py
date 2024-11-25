import os
import pandas as pd
from faker import Faker
import random

# Inicializar Faker
fake = Faker()

# Directorio base para los archivos generados
base_dir = (r"C:\Users\Familia\BD\Data_p")

# Variables globales para almacenar datos generados
personas = []
trabajadores = []
usuarios = []
conductores = []
guias = []
buses = []
rutas = []
estaciones = []
tarjetas = []
viajes = []
paradas = []
recargas = []
historial_manejos = []

# Crear carpetas organizadas por tamaño de datos
def create_directories():
    sizes = ['1000', '10000', '100000', '1000000']
    for size in sizes:
        directory = os.path.join(base_dir, size)
        os.makedirs(directory, exist_ok=True)

# Funciones de generación de datos
def generate_persona_data(size):
    global personas
    personas = [
        {"dni": fake.unique.random_number(digits=8, fix_len=True),
         "nombre": fake.first_name(),
         "apellido": fake.last_name(),
         "email": fake.unique.email(),
         "genero": random.choice(['F', 'M'])}
        for _ in range(size)
    ]
    return pd.DataFrame(personas)

def generate_trabajador_data(size):
    global trabajadores
    trabajadores = [{"dni": persona["dni"]} for persona in personas]
    return pd.DataFrame(trabajadores)

def generate_usuario_data(size):
    global usuarios
    usuarios = [{"dni": persona["dni"]} for persona in personas]
    return pd.DataFrame(usuarios)

def generate_conductor_data(size):
    global conductores
    conductores = [{"dni": persona["dni"], "licencia": fake.unique.random_number(digits=9, fix_len=True)} for persona in personas]
    return pd.DataFrame(conductores)

def generate_guia_data(size):
    global guias
    guias = [{"dni": persona["dni"], "nombre_estacion": fake.word()} for persona in personas]
    return pd.DataFrame(guias)

def generate_bus_data(size):
    global buses
    buses = [{"placa": fake.license_plate(), "aforo_bus": random.randint(31, 79), "modelo": fake.word()} for _ in range(size)]
    return pd.DataFrame(buses)

def generate_ruta_data(size):
    global rutas
    rutas = [{"nombre_ruta": fake.word(), "nro_estaciones": random.randint(6, 55), "tiempo_recorrido": random.randint(31, 120)} for _ in range(size)]
    return pd.DataFrame(rutas)

def generate_estacion_data(size):
    global estaciones
    estaciones = [{"nombre_estacion": fake.word(), "distrito": random.choice(['Carabayllo', 'Comas', 'Independencia', 'San Martín de Porres', 'Rímac','Breña', 'Lima', 'Chorrillos', 'La Victoria', 'Lince', 'San Isidro',
 'Barranco', 'Miraflores', 'Surquillo']), "aforo_estacion": random.randint(31, 299)} for _ in range(size)]
    return pd.DataFrame(estaciones)

def generate_tarjeta_data(size):
    global tarjetas
    tarjetas = [{"id_tarjeta": fake.unique.uuid4(), "saldo": 0, "dni": random.choice(personas)["dni"]} for _ in range(size)]
    return pd.DataFrame(tarjetas)

def generate_viaje_data(size):
    global viajes
    viajes = [{"id_viaje": i + 1, "nombre_ruta": random.choice(rutas)["nombre_ruta"], "id_tarjeta": random.choice(tarjetas)["id_tarjeta"]} for i in range(size)]
    return pd.DataFrame(viajes)

def generate_parada_data(size):
    global paradas
    paradas = [{"placa": random.choice(buses)["placa"], "nombre_estacion": random.choice(estaciones)["nombre_estacion"], "fecha_parada": fake.date_time_this_year()} for _ in range(size)]
    return pd.DataFrame(paradas)

def generate_recarga_data(size):
    global recargas
    recargas = [{"id_tarjeta": random.choice(tarjetas)["id_tarjeta"], "fecha_recarga": fake.date_time_this_year(), "monto": random.uniform(0.21, 100)} for _ in range(size)]
    return pd.DataFrame(recargas)

def generate_historial_manejo_data(size):
    global historial_manejos
    historial_manejos = [{"dni": random.choice(conductores)["dni"], "placa ": random.choice(buses)["placa"], "nombre_ruta": random.choice(rutas)["nombre_ruta"], "fecha_historial": fake.date_time_this_year()} for _ in range(size)]
    return pd.DataFrame(historial_manejos)

# Generar datos para todas las tablas y guardarlos
def generate_and_save_data():
    sizes = [100000]  # Ajusta el tamaño según sea necesario
    functions = [
        ("Persona", generate_persona_data),
        ("Trabajador", generate_trabajador_data),
        ("Usuarios", generate_usuario_data),
        ("Conductor", generate_conductor_data),
        ("Guia", generate_guia_data),
        ("Bus", generate_bus_data),
        ("Ruta", generate_ruta_data),
        ("Estacion", generate_estacion_data),
        ("Tarjeta", generate_tarjeta_data),
        ("Viaje", generate_viaje_data),
        ("Parada", generate_parada_data),
        ("Recarga", generate_recarga_data),
        ("Historial de manejos", generate_historial_manejo_data)
    ]

    for size in sizes:
        folder = os.path.join(base_dir, str(size))
        for table_name, func in functions:
            print(f"Generando datos para {table_name} con {size} registros...")
            data = func(size)
            file_path = os.path.join(folder, f"{table_name.lower()}.csv")
            data.to_csv(file_path, index=False, sep=',', quoting=1)
            print(f"Archivo generado: {file_path}")

# Crear carpetas y generar datos
create_directories()
generate_and_save_data()