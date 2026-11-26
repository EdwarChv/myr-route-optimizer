-- Ejecutar únicamente en la base dedicada del proyecto.
BEGIN;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgrouting;
CREATE SCHEMA IF NOT EXISTS myr;
CREATE TABLE IF NOT EXISTS myr.deposito (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre text NOT NULL,
    ubicacion geometry(Point, 4326) NOT NULL
);
CREATE TABLE IF NOT EXISTS myr.vehiculo (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo text NOT NULL UNIQUE,
    capacidad_kg numeric(10,2) NOT NULL CHECK (capacidad_kg > 0),
    activo boolean NOT NULL DEFAULT true
);
CREATE TABLE IF NOT EXISTS myr.carga (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    origen text NOT NULL,
    fecha timestamptz NOT NULL DEFAULT now(),
    total integer NOT NULL CHECK (total >= 0)
);
CREATE TABLE IF NOT EXISTS myr.pedido (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    carga_id bigint NOT NULL REFERENCES myr.carga(id),
    codigo text NOT NULL,
    ubicacion geometry(Point,4326) NOT NULL,
    peso_kg numeric(10,2) NOT NULL CHECK (peso_kg > 0),
    ventana_inicio time NOT NULL,
    ventana_fin time NOT NULL,
    servicio_min integer NOT NULL CHECK (servicio_min >= 0),
    CHECK (ventana_inicio < ventana_fin),
    UNIQUE (carga_id, codigo)
);
CREATE INDEX IF NOT EXISTS pedido_ubicacion_gix ON myr.pedido USING gist (ubicacion);
CREATE TABLE IF NOT EXISTS myr.grafo_version (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fuente text NOT NULL,
    fecha_datos date NOT NULL,
    descripcion text,
    creado timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS myr.ejecucion (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    carga_id bigint REFERENCES myr.carga(id),
    grafo_id bigint REFERENCES myr.grafo_version(id),
    creada timestamptz NOT NULL DEFAULT now(),
    estado text NOT NULL,
    parametros jsonb NOT NULL DEFAULT '{}'::jsonb
);
INSERT INTO myr.deposito(nombre, ubicacion)
SELECT 'MyR Operador Logístico', ST_SetSRID(ST_MakePoint(-76.9943621,-12.0695081),4326)
WHERE NOT EXISTS (SELECT 1 FROM myr.deposito WHERE nombre = 'MyR Operador Logístico');
INSERT INTO myr.vehiculo(codigo, capacidad_kg)
SELECT 'CAM-' || lpad(n::text,2,'0'), 800 FROM generate_series(1,15) AS n
ON CONFLICT (codigo) DO NOTHING;
COMMIT;
