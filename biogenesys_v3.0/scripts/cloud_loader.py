import pandas as pd
from sqlalchemy import create_engine
import os
import time

# Importamos el archivo que contiene las credenciales (DB_HOST, DB_USER, etc.)
import credentials_bio # type: ignore

# ####################################################################
# 1. PARÁMETROS DE CONEXIÓN IMPORTADOS DESDE SECRETS_DB.PY
# ####################################################################
DB_NAME = credentials_bio.DB_NAME       
DB_USER = credentials_bio.DB_USER
DB_PASSWORD = credentials_bio.DB_PASSWORD 
DB_HOST = credentials_bio.DB_HOST 
DB_PORT = credentials_bio.DB_PORT                 

# RUTA COMPLETA Y NOMBRE DE TU ARCHIVO CSV DE DATOS
CSV_FILE_PATH = r'C:\Users\Bruger\Desktop\biogenesys_saga\biogenesys_v2.0\data_procesada_biogenesys_v2.csv'

# Construir la cadena de conexión de SQLAlchemy
CONN_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Línea de DEBUG para confirmar que estamos usando la IP directa y no el host truncado
print(f"DEBUG: Intentando conectar a: {DB_HOST}:{DB_PORT} con usuario: {DB_USER}")

try:
    ENGINE = create_engine(CONN_STRING)
except Exception as e:
    print(f"❌ ERROR CRÍTICO DE CONEXIÓN: No se pudo crear el motor de base de datos. Verifique IP y Firewall. Error: {e}")
    exit()

# ####################################################################
# 2. LECTURA Y TRANSFORMACIÓN DEL CSV
# ####################################################################

print("1. Leyendo y transformando el archivo CSV...")
try:
    df_full = pd.read_csv(CSV_FILE_PATH)
    df_full['date'] = pd.to_datetime(df_full['date'])
    
    # Columnas Clave
    PK_COLS = ['location_key']
    
    # Definición de columnas para cada Dimensión y la tabla Fact
    cols_country = PK_COLS + ['country_code', 'country_name']
    cols_population = PK_COLS + ['population', 'population_male', 'population_female', 'population_rural', 'population_urban', 'population_density', 'population_largest_city', 'population_age_10_39', 'population_age_40_69', 'population_age_70_plus']
    cols_geography = PK_COLS + ['latitude', 'longitude', 'area_sq_km', 'area_rural_sq_km', 'area_urban_sq_km', 'average_temperature_celsius', 'minimum_temperature_celsius', 'maximum_temperature_celsius', 'rainfall_mm', 'relative_humidity']
    cols_health = PK_COLS + ['nurses_per_1000', 'physicians_per_1000', 'smoking_prevalence', 'diabetes_prevalence', 'infant_mortality_rate', 'adult_male_mortality_rate', 'adult_female_mortality_rate', 'pollution_mortality_rate', 'comorbidity_mortality_rate', 'life_expectancy']
    cols_socioeconomic = PK_COLS + ['human_development_index', 'gdp_usd', 'gdp_per_capita_usd']
    
    # Creación y desduplicación de DataFrames de Dimensión
    df_dim_country = df_full[cols_country].drop_duplicates(subset=['location_key']).set_index('location_key')
    df_dim_population = df_full[cols_population].drop_duplicates(subset=['location_key']).set_index('location_key')
    df_dim_geography = df_full[cols_geography].drop_duplicates(subset=['location_key']).set_index('location_key')
    df_dim_health = df_full[cols_health].drop_duplicates(subset=['location_key']).set_index('location_key')
    df_dim_socioeconomic = df_full[cols_socioeconomic].drop_duplicates(subset=['location_key']).set_index('location_key')
    
    # Creación del DataFrame de Hechos (Fact)
    df_fact = df_full[['location_key', 'date', 'new_confirmed', 'new_deceased', 'cumulative_confirmed', 'cumulative_deceased', 'cumulative_vaccine_doses_administered', 'casos_activos_estimados', 'muertes_por_1000', 'casos_por_1000', 'vacunas_por_1000', 'tasa_letalidad_por_1000', 'tasa_recuperacion_por_1000', 'casos_activos_por_1000', 'letalidad']].copy()
    
    print("Separación de datos completada.")

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo en la ruta: {CSV_FILE_PATH}")
    exit()
except Exception as e:
    print(f"Error en la lectura/transformación: {e}")
    exit()

# ####################################################################
# 3. CARGA DE DATOS (LOAD) A AWS RDS
# ####################################################################

def load_data(df, table_name):
    """Función que carga un DataFrame a la base de datos."""
    print(f"\nCargando datos en la tabla: {table_name}...")
    start_time = time.time()
    try:
        df.to_sql(table_name, ENGINE, schema='public', if_exists='append', index=True if 'location_key' in df.index.names else False )
        elapsed_time = time.time() - start_time
        print(f"✔️ {df.shape[0]} filas cargadas en {table_name} en {elapsed_time:.2f} segundos.")
    except Exception as e:
        print(f"❌ ERROR al cargar {table_name}. Error: {e}")
        # No usamos 'pass' aquí, ya que el motor debe estar conectado antes de llegar a este punto
        # Si falla aquí, es probablemente por una clave duplicada o un timeout de la conexión.
        pass 

# Carga de Dimensiones
load_data(df_dim_country, 'Dim_Country')
load_data(df_dim_population, 'Dim_Population')
load_data(df_dim_geography, 'Dim_Geography')
load_data(df_dim_health, 'Dim_Health')
load_data(df_dim_socioeconomic, 'Dim_Socioeconomic')

# Carga de la Tabla de Hechos
load_data(df_fact, 'Fact')

print("\n🎉 Proceso ETL finalizado. La base de datos RDS ha sido cargada.")