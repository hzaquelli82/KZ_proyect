# Proyecto de Migración Excel a PostgreSQL

Este repositorio contiene las herramientas y planes para migrar el sistema de gestión actual (Excel) a una base de datos PostgreSQL.

## Estructura del Proyecto

*   `CRONOGRAMA_PROYECTO.md`: El plan de trabajo detallado para 4 semanas (4hs/día).
*   `schema.sql`: Definición de la estructura de la base de datos (Tablas, Claves foráneas).
*   `scripts/`: Scripts de Python para la migración de datos (ETL).
*   `db/`: Scripts de utilidad para la base de datos.
*   `reporte_estadist.xlsx`: Datos de referencia (Ubigeo, Población).

## Cómo empezar

### 1. Preparar el Entorno

Se recomienda usar un entorno virtual de Python.

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r scripts/requirements.txt
```

### 2. Configurar la Base de Datos Local

Asegúrate de tener PostgreSQL instalado y ejecutándose.

```bash
# Dar permisos de ejecución
chmod +x db/setup_db.sh

# Ejecutar script de configuración (ajustar variables en el script si es necesario)
cd db
./setup_db.sh
cd ..
```

### 3. Ejecutar la Migración de Datos

El script principal de ETL leerá el archivo Excel (`data_privada/Reporte.xlsx` o configurable) y cargará los datos en la base de datos local.

```bash
# Configurar variables de entorno si tu BD tiene contraseña
export DB_PASS="tu_contraseña"

# Ejecutar script
python3 scripts/etl_pipeline.py
```

## Estado del Proyecto

*   [x] Diseño de Esquema de Base de Datos (`schema.sql`).
*   [x] Cronograma de Trabajo (`CRONOGRAMA_PROYECTO.md`).
*   [x] Pipeline ETL Inicial (Clientes y Ubicaciones).
*   [ ] Implementación ETL Ventas y Detalles.
*   [ ] Selección y Despliegue en Hosting.
