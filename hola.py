import os
import pandas as pd
from faker import Faker
import random
import uuid
import datetime

# Inicializar Faker
fake = Faker()

# Directorio base para los archivos generados
base_dir = r"C:\Users\Familia\BD\Data_p"

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
recargas = []
paradas = []
historial_manejos = []
viajes = []

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

def generate_trabajador_and_usuario_data():
    global trabajadores, usuarios
    trabajadores_dnis = random.sample(personas, 2000)
    usuarios_dnis = random.sample([persona for persona in personas if persona not in trabajadores_dnis], 3000)

    trabajadores = [{"dni": trabajador["dni"]} for trabajador in trabajadores_dnis]
    usuarios = [{"dni": usuario["dni"]} for usuario in usuarios_dnis]

    return pd.DataFrame(trabajadores), pd.DataFrame(usuarios)

def generate_conductor_and_guia_data():
    global conductores, guias
    conductores_dnis = random.sample(trabajadores, 1000)
    guias_dnis = random.sample([trabajador for trabajador in trabajadores if trabajador not in conductores_dnis], 1000)

    conductores = [
        {"dni": conductor["dni"], "licencia": fake.unique.random_number(digits=9, fix_len=True)}
        for conductor in conductores_dnis
    ]
    guias = [
        {"dni": guia["dni"], "nombre_estacion": random.choice(estaciones)["nombre_estacion"]}
        for guia in guias_dnis
    ]

    return pd.DataFrame(conductores), pd.DataFrame(guias)
def generate_bus_data(size):
    global buses
    buses = [{"placa": fake.unique.license_plate(), "aforo_bus": random.randint(31, 79), "modelo": fake.word()} for _ in range(size)]
    return pd.DataFrame(buses)

def generate_ruta_data(size):
    global rutas
    rutas = [
        {
            "nombre_ruta": str(uuid.uuid4())[:15],
            "nro_estaciones": random.randint(6, 55),
            "tiempo_recorrido": random.randint(31, 120)
        }
        for _ in range(size)
    ]
    return pd.DataFrame(rutas)

def generate_estacion_data(size):
    global estaciones
    estaciones = [
        {
            "nombre_estacion": str(uuid.uuid4())[:15],
            "distrito": random.choice([
                'Carabayllo', 'Comas', 'Independencia', 'San Martin de Porres', 'Rimac',
                'Brena', 'Lima', 'Chorrillos', 'La Victoria', 'Lince', 'San Isidro',
                'Barranco', 'Miraflores', 'Surquillo'
            ]),
            "aforo_estacion": random.randint(31, 299)
        }
        for _ in range(size)
    ]
    return pd.DataFrame(estaciones)

def generate_tarjeta_data():
    global tarjetas
    tarjetas = [
        {
            "id_tarjeta": str(uuid.uuid4()),
            "saldo": round(random.uniform(0, 100), 2),
            "dni": usuario["dni"]
        }
        for usuario in usuarios
    ]
    return pd.DataFrame(tarjetas)

def generate_recarga_data(size):
    global recargas
    recargas = [
        {
            "id_tarjeta": random.choice(tarjetas)["id_tarjeta"],
            "fecha_recarga": fake.date_time_this_year(),
            "monto": round(random.uniform(0.2, 100), 2)
        }
        for _ in range(size)
    ]
    return pd.DataFrame(recargas)

def generate_parada_data(size):
    global paradas
    paradas = [
        {
            "placa": random.choice(buses)["placa"],
            "nombre_estacion": random.choice(estaciones)["nombre_estacion"],
            "fecha_parada": fake.date_time_this_year()
        }
        for _ in range(size)
    ]
    return pd.DataFrame(paradas)

def generate_historial_manejo_data(size):
    global historial_manejos
    historial_manejos = [
        {
            "dni": random.choice(conductores)["dni"],
            "placa": random.choice(buses)["placa"],
            "nombre_ruta": random.choice(rutas)["nombre_ruta"],
            "fecha_historial": datetime.datetime.fromtimestamp(fake.date_time_this_year().timestamp())  # Convertir a formato timestamp
        }
        for _ in range(size)
    ]
    return pd.DataFrame(historial_manejos)


def generate_viaje_data(size):
    global viajes
    viajes = [
        {
            "id_viaje": i + 1,
            "nombre_ruta": random.choice(rutas)["nombre_ruta"],
            "id_tarjeta": random.choice(tarjetas)["id_tarjeta"]
        }
        for i in range(size)
    ]
    return pd.DataFrame(viajes)

def generate_and_save_data():
    folder = os.path.join(base_dir, '1000')
    os.makedirs(folder, exist_ok=True)

    print("Generando datos...")

    # Generar primero las estaciones
    estaciones_df = generate_estacion_data(1000)

    # Luego generar las demás entidades
    personas_df = generate_persona_data(5000)
    trabajadores_df, usuarios_df = generate_trabajador_and_usuario_data()
    conductores_df, guias_df = generate_conductor_and_guia_data()  # Aquí ahora sí pueden asignarse estaciones a los guías
    tarjetas_df = generate_tarjeta_data()
    recargas_df = generate_recarga_data(2000)
    buses_df = generate_bus_data(1000)
    rutas_df = generate_ruta_data(1000)
    paradas_df = generate_parada_data(1000)
    historial_df = generate_historial_manejo_data(1000)
    viajes_df = generate_viaje_data(1000)

    # Guardar datos
    for table_name, data in [
        ("Persona", personas_df), ("Trabajador", trabajadores_df),
        ("Usuarios", usuarios_df), ("Conductor", conductores_df),
        ("Guia", guias_df), ("Tarjeta", tarjetas_df), ("Recarga", recargas_df),
        ("Bus", buses_df), ("Ruta", rutas_df), ("Estacion", estaciones_df),
        ("Parada", paradas_df), ("HistorialManejos", historial_df),
        ("Viaje", viajes_df)
    ]:
        file_path = os.path.join(folder, f"{table_name.lower()}.csv")
        data.to_csv(file_path, index=False, sep=',', quoting=1)
        print(f"Archivo generado: {file_path}")

# Crear carpetas y generar datos
create_directories()
generate_and_save_data()
