import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import os
import sys

# Configuración de Conexión a Base de Datos
# Se recomienda usar variables de entorno para credenciales
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'kz_project')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Ruta del archivo Excel (ajustar según ubicación real)
EXCEL_PATH = 'data_privada/Reporte.xlsx'
# Nota: Si se usa el archivo de ejemplo del repo:
# EXCEL_PATH = 'reporte_estadist.xlsx'

def get_db_connection():
    """Establece conexión con la base de datos."""
    try:
        engine = create_engine(DATABASE_URL)
        print("Conexión a BD establecida.")
        return engine
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        sys.exit(1)

def load_excel_data(filepath):
    """Carga el archivo Excel y devuelve un diccionario de DataFrames."""
    if not os.path.exists(filepath):
        print(f"Error: El archivo {filepath} no existe.")
        return None

    print(f"Cargando archivo Excel: {filepath} ...")
    try:
        dfs = pd.read_excel(filepath, sheet_name=None)
        print("Hojas encontradas:", dfs.keys())
        return dfs
    except Exception as e:
        print(f"Error leyendo Excel: {e}")
        return None

def clean_and_load_ubicaciones(df_clientes, engine):
    """
    Extrae ubicaciones únicas de la hoja de Clientes y las carga.
    Asume columnas: 'Departamento', 'Provincia', 'Distrito'
    """
    print("Procesando Ubicaciones...")
    if 'Departamento' not in df_clientes.columns:
        print("Advertencia: Columna 'Departamento' no encontrada en Clientes.")
        return

    # Seleccionar columnas relevantes y eliminar duplicados
    ubicaciones = df_clientes[['Departamento', 'Provincia', 'Distrito']].drop_duplicates().dropna(how='all')

    # Limpieza básica
    ubicaciones['Departamento'] = ubicaciones['Departamento'].str.upper().str.strip()
    ubicaciones['Provincia'] = ubicaciones['Provincia'].str.upper().str.strip()
    ubicaciones['Distrito'] = ubicaciones['Distrito'].str.upper().str.strip()

    ubicaciones = ubicaciones.drop_duplicates(subset=['Departamento', 'Provincia', 'Distrito'])

    # Cargar a BD (usando ON CONFLICT DO NOTHING si fuera raw SQL, pero con pandas es append)
    # Para evitar duplicados en cargas sucesivas, lo ideal es leer las existentes primero.

    # Leer ubicaciones existentes
    existing_ub = pd.read_sql("SELECT departamento, provincia, distrito FROM ubicaciones", engine)

    # Renombrar columnas de BD para coincidir con Excel para el merge
    existing_ub.columns = ['Departamento', 'Provincia', 'Distrito']

    # Filtrar las que ya existen (anti-join)
    # Esto es una simplificación. En producción se puede usar tablas temporales.
    merged = ubicaciones.merge(existing_ub, on=['Departamento', 'Provincia', 'Distrito'], how='left', indicator=True)
    new_ubicaciones = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_ubicaciones.empty:
        new_ubicaciones.columns = ['departamento', 'provincia', 'distrito'] # Match DB columns
        new_ubicaciones.to_sql('ubicaciones', engine, if_exists='append', index=False)
        print(f"Insertadas {len(new_ubicaciones)} nuevas ubicaciones.")
    else:
        print("No hay nuevas ubicaciones para insertar.")

def clean_and_load_clientes(df_clientes, engine):
    """
    Transforma y carga datos de clientes.
    """
    print("Procesando Clientes...")
    # Columnas esperadas del Excel (basado en notebook):
    # 'ID Cliente', 'Nombre completo', 'Celular', 'Correo', 'Departamento', etc.

    # Copia para no modificar original
    df = df_clientes.copy()

    # Limpieza
    df['ID Cliente'] = pd.to_numeric(df['ID Cliente'], errors='coerce')
    df = df.dropna(subset=['Nombre completo']) # Nombre es obligatorio

    # Mapeo de Ubicación (necesitamos el ID de la tabla ubicaciones)
    # Leemos la tabla ubicaciones completa de la BD para hacer el join
    df_ub_db = pd.read_sql("SELECT id_ubicacion, departamento, provincia, distrito FROM ubicaciones", engine)

    # Normalizar para el join
    df['Departamento'] = df['Departamento'].str.upper().str.strip()
    df['Provincia'] = df['Provincia'].str.upper().str.strip()
    df['Distrito'] = df['Distrito'].str.upper().str.strip()

    # Join para obtener id_ubicacion
    df_merged = df.merge(df_ub_db,
                         left_on=['Departamento', 'Provincia', 'Distrito'],
                         right_on=['departamento', 'provincia', 'distrito'],
                         how='left')

    # Preparar DataFrame final para insertar
    df_final = pd.DataFrame()
    # Mapeo de columnas Excel -> BD
    df_final['nombre_completo'] = df_merged['Nombre completo']
    df_final['nombre_saludo'] = df_merged['Nombre']
    df_final['celular'] = df_merged['Celular'].astype(str)
    df_final['correo'] = df_merged['Correo']
    df_final['fecha_cumpleanos'] = pd.to_datetime(df_merged['Cumpleaños'], errors='coerce')
    df_final['origen'] = df_merged['Origen']
    df_final['sub_origen'] = df_merged['Sub Origen']
    df_final['direccion_calle'] = df_merged['Dirección']
    df_final['id_ubicacion'] = df_merged['id_ubicacion']
    df_final['comentario_google'] = df_merged['Comentario en google'].apply(lambda x: True if str(x).lower() == 'si' else False)
    df_final['nota'] = df_merged['Nota']

    # Insertar
    # Ojo: Clientes puede tener duplicados en Excel. Se asume que Nombre Completo o ID debería ser único?
    # Por ahora insertamos todo (append).

    try:
        df_final.to_sql('clientes', engine, if_exists='append', index=False)
        print(f"Insertados {len(df_final)} clientes.")
    except Exception as e:
        print(f"Error insertando clientes: {e}")


def main():
    engine = get_db_connection()

    dfs = load_excel_data(EXCEL_PATH)
    if dfs is None:
        print("No se pudieron cargar los datos. Abortando.")
        return

    # Ejecutar pipeline por fases
    if 'Clientes' in dfs:
        clean_and_load_ubicaciones(dfs['Clientes'], engine)
        clean_and_load_clientes(dfs['Clientes'], engine)
    else:
        print("Hoja 'Clientes' no encontrada.")

    # Aquí se agregarían las funciones para Ventas, Productos, etc.
    # clean_and_load_productos(dfs['Ventas'], engine)
    # clean_and_load_ventas(dfs['Ventas'], engine)

if __name__ == "__main__":
    main()
