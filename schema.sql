-- Schema for KZ Project
-- Generated based on diccionario_datos.txt
-- Normalization Level: 3NF
-- Part of Project Schedule Phase 1

DROP TABLE IF EXISTS detalle_ventas CASCADE;
DROP TABLE IF EXISTS deliveries CASCADE;
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS gastos CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS sub_categorias CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS marcas CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS ubicaciones CASCADE;
DROP TABLE IF EXISTS empresas_delivery CASCADE;
DROP TABLE IF EXISTS proveedores CASCADE;

-- 1. Ubicaciones (Normalized Geography)
CREATE TABLE ubicaciones (
    id_ubicacion SERIAL PRIMARY KEY,
    departamento VARCHAR(100) NOT NULL,
    provincia VARCHAR(100),
    distrito VARCHAR(100),
    CONSTRAINT uq_ubicacion UNIQUE (departamento, provincia, distrito)
);

-- 2. Clientes
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    nombre_saludo VARCHAR(100),
    celular VARCHAR(50),
    dni VARCHAR(20),
    correo VARCHAR(255),
    fecha_cumpleanos DATE,
    origen VARCHAR(100), -- How they found the company
    sub_origen VARCHAR(100),
    direccion_calle VARCHAR(255),
    id_ubicacion INTEGER REFERENCES ubicaciones(id_ubicacion),
    comentario_google BOOLEAN,
    nota TEXT
);

-- 3. Categorias & Subcategorias
CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE sub_categorias (
    id_sub_categoria SERIAL PRIMARY KEY,
    id_categoria INTEGER REFERENCES categorias(id_categoria),
    nombre VARCHAR(100) NOT NULL
);

-- 4. Marcas
CREATE TABLE marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- 5. Productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    abreviatura VARCHAR(50),
    id_marca INTEGER REFERENCES marcas(id_marca),
    id_sub_categoria INTEGER REFERENCES sub_categorias(id_sub_categoria),
    tipo_registro VARCHAR(50), -- From 'Tipo' column
    sub_tipo VARCHAR(100), -- From 'Sub Tipo' column
    codigo_ean13 VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'Activado', -- Activado/Desactivado
    
    -- Costing
    costo_prima_sin_igv DECIMAL(10,2),
    igv_compra_prima DECIMAL(10,2),
    costo_etiqueta DECIMAL(10,2),
    costo_envoltura DECIMAL(10,2),
    costo_produccion DECIMAL(10,2),
    costo_unitario_total DECIMAL(10,2),
    
    -- Pricing
    precio_venta_base DECIMAL(10,2),
    precio_venta_sugerido DECIMAL(10,2),
    precio_venta_delivery DECIMAL(10,2),
    precio_venta_mayor DECIMAL(10,2)
);

-- 6. Ventas (Header)
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    fecha_entrega DATE,
    estado_entrega VARCHAR(50), -- Entregado, Pendiente
    estado_pago VARCHAR(50), -- Cancelado, Pendiente
    medio_pago VARCHAR(50),
    fecha_pago DATE,
    comprobante_tipo VARCHAR(50),
    comprobante_numero VARCHAR(50),
    monto_comprobante DECIMAL(10,2),
    ganancia_neta DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Detalle Ventas
CREATE TABLE detalle_ventas (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL, -- Snapshot of price at time of sale
    descuento DECIMAL(10,2) DEFAULT 0,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario - descuento) STORED
);

-- 8. Empresas Delivery
CREATE TABLE empresas_delivery (
    id_empresa_delivery SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- 9. Deliveries
CREATE TABLE deliveries (
    id_delivery SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_empresa_delivery INTEGER REFERENCES empresas_delivery(id_empresa_delivery),
    fecha_envio DATE,
    costo_delivery DECIMAL(10,2),
    direccion_entrega VARCHAR(255),
    id_ubicacion INTEGER REFERENCES ubicaciones(id_ubicacion),
    numero_factura VARCHAR(50),
    fecha_factura DATE,
    en_ruta BOOLEAN,
    comentario TEXT
);

-- 10. Proveedores
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- 11. Gastos
CREATE TABLE gastos (
    id_gasto SERIAL PRIMARY KEY,
    fecha_ingreso DATE,
    id_proveedor INTEGER REFERENCES proveedores(id_proveedor),
    descripcion VARCHAR(255),
    tipo_gasto VARCHAR(50), -- From 'Tipo'
    categoria_gasto VARCHAR(50), -- From 'Categoría'
    monto_total DECIMAL(10,2),
    numero_factura VARCHAR(50),
    fecha_factura DATE,
    estado_pago VARCHAR(50)
);
