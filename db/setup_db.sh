#!/bin/bash
# Script para inicializar la base de datos (Requiere cliente psql instalado)

DB_NAME="kz_project"
DB_USER="postgres"

echo "Creando base de datos $DB_NAME..."
# Intentar crear BD (puede fallar si ya existe)
createdb -U $DB_USER $DB_NAME || echo "Base de datos ya existe o error al crear."

echo "Aplicando esquema..."
psql -U $DB_USER -d $DB_NAME -f ../schema.sql

if [ $? -eq 0 ]; then
    echo "Esquema aplicado exitosamente."
else
    echo "Error aplicando el esquema."
fi
