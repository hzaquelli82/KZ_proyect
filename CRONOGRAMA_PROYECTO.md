# Cronograma de Proyecto: Migración de Excel a PostgreSQL

Este cronograma está diseñado para un esfuerzo de **4 horas diarias** durante **4 semanas**. El objetivo es migrar un sistema de seguimiento complejo basado en Excel a una base de datos relacional PostgreSQL.

## Fase 1: Análisis, Diseño y Configuración (Semana 1)

El objetivo de esta semana es establecer los cimientos del proyecto y asegurar que la estructura de datos sea sólida.

*   **Día 1: Configuración del Entorno y Base de Datos Local**
    *   Instalar Python, PostgreSQL y herramientas de administración (pgAdmin o DBeaver).
    *   Crear un entorno virtual de Python (`venv`) e instalar librerías (`pandas`, `sqlalchemy`, `psycopg2`, `openpyxl`).
    *   Inicializar la base de datos local `kz_project`.
    *   Ejecutar el script `schema.sql` para crear las tablas.
    *   *Entregable:* Base de datos vacía funcionando localmente.

*   **Día 2: Análisis de Datos "Maestros" (Clientes y Ubicaciones)**
    *   Revisar la hoja 'Clientes' y 'Reporte estadístico' (Ubicaciones).
    *   Identificar inconsistencias (nombres mal escritos, departamentos faltantes).
    *   Diseñar la estrategia de limpieza para direcciones y ubigeos.
    *   Actualizar `schema.sql` si se encuentran nuevos campos necesarios.

*   **Día 3: Desarrollo ETL - Ubicaciones y Clientes**
    *   Escribir script Python para extraer y normalizar `Ubicaciones` (Departamento, Provincia, Distrito).
    *   Escribir script para cargar `Clientes`, asegurando que se vinculen correctamente a los IDs de `Ubicaciones`.
    *   Manejo de duplicados en Clientes.

*   **Día 4: Análisis de Productos y Categorías**
    *   Revisar hojas de productos (si existen en el Excel) o extraer productos únicos de la hoja 'Ventas'.
    *   Definir jerarquía: Categoría -> Subcategoría -> Marca -> Producto.
    *   Mapear columnas de costos y precios.

*   **Día 5: Desarrollo ETL - Productos**
    *   Implementar carga de `Categorias`, `Sub_Categorias`, `Marcas`.
    *   Implementar carga de `Productos`.
    *   Validar que los SKUs sean únicos.

## Fase 2: Datos Transaccionales y Lógica de Negocio (Semana 2)

Esta semana se enfoca en la parte más compleja: las ventas y el historial de movimientos.

*   **Día 1: Análisis de Ventas y Detalle**
    *   Estudiar la hoja 'Ventas'. Entender la relación entre el encabezado (Fecha, Cliente, Pago) y el detalle (Producto, Cantidad, Precio).
    *   Identificar cómo agrupar filas para formar una única "Venta" (ID de venta vs ID de producto).

*   **Día 2: Desarrollo ETL - Cabecera de Ventas**
    *   Script para agrupar ventas y crear registros en la tabla `ventas`.
    *   Mapeo de estados (Entregado, Pendiente, Cancelado).
    *   Vinculación con `clientes`.

*   **Día 3: Desarrollo ETL - Detalle de Ventas**
    *   Script para insertar en `detalle_ventas`.
    *   Búsqueda de `id_producto` basado en el nombre/SKU del Excel.
    *   Cálculo y validación de subtotales (Cantidad * Precio).

*   **Día 4: Logística y Delivery**
    *   Análisis de la hoja 'Delivery' y 'Empresas Delivery'.
    *   Carga de `empresas_delivery`.
    *   Carga de la tabla `deliveries`, vinculando con `ventas`.

*   **Día 5: Gastos y Proveedores**
    *   Análisis y carga de la hoja 'Gastos'.
    *   Normalización de `proveedores`.
    *   Carga de tabla `gastos`.

## Fase 3: Integración, Validación e Investigación de Hosting (Semana 3)

*   **Día 1: Ejecución Completa y Depuración**
    *   Ejecutar el pipeline ETL completo (todas las tablas en orden).
    *   Resolver errores de integridad referencial (Foreign Keys).
    *   Medir tiempo de ejecución.

*   **Día 2: Validación de Datos (Quality Assurance)**
    *   Comparar totales (Suma de ventas mes a mes) entre Excel y SQL.
    *   Verificar conteo de clientes.
    *   Corregir scripts de limpieza si los números no cuadran.

*   **Día 3: Investigación de Hosting (Tarea Solicitada)**
    *   Evaluar opciones para alojar la base de datos PostgreSQL:
        *   **Opción A (Cloud Gestionado):** AWS RDS, Google Cloud SQL, Azure (Costo $$$, Alta disponibilidad).
        *   **Opción B (PaaS):** Heroku Postgres, Render, Railway, Fly.io (Costo $-$$, Fácil uso).
        *   **Opción C (Serverless):** Supabase, Neon (Capa gratuita generosa, bueno para empezar).
    *   Seleccionar proveedor basado en presupuesto y conocimientos técnicos.

*   **Día 4: Configuración de Hosting**
    *   Crear cuenta en el proveedor seleccionado (ej. Supabase o Render).
    *   Provisionar la instancia de base de datos.
    *   Obtener credenciales de conexión (URI).

*   **Día 5: Despliegue de Esquema Remoto**
    *   Conectar herramienta local (DBeaver) a la BD remota.
    *   Ejecutar `schema.sql` en la nube.
    *   Ajustar configuraciones de seguridad (IP whitelist si es necesario).

## Fase 4: Migración Final y Documentación (Semana 4)

*   **Día 1: Carga de Datos en Producción**
    *   Configurar script ETL para apuntar a la BD remota.
    *   Ejecutar carga masiva.
    *   Verificar logs de errores.

*   **Día 2: Optimización**
    *   Crear índices adicionales en columnas de búsqueda frecuente (ej. `email`, `sku`, `fecha_venta`).
    *   Crear Vistas (Views) para reportes comunes (ej. "Ventas por Mes", "Mejores Clientes").

*   **Día 3: Documentación Técnica**
    *   Documentar el proceso de carga ("Cómo actualizar los datos").
    *   Explicar el modelo de datos (Diccionario de datos actualizado).

*   **Día 4: Pruebas de Usuario / Capacitación**
    *   Simular consultas reales de negocio.
    *   Conectar Excel o PowerBI a la base de datos para verificar que se pueden leer los reportes.

*   **Día 5: Cierre del Proyecto**
    *   Backup final de la base de datos.
    *   Revisión de pendientes.
    *   Planificación de siguientes pasos (Desarrollo de App web, reportes automáticos, etc.).
