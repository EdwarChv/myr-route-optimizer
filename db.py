"""Conexión local explícita; no se establece al importar el módulo."""
import psycopg


def comprobar_conexion(config):
    """Comprueba identidad y extensiones, sin modificar la base."""
    with psycopg.connect(**dict(config), connect_timeout=5) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user")
            database, user = cursor.fetchone()
            cursor.execute("SELECT extname, extversion FROM pg_extension WHERE extname IN ('postgis', 'pgrouting') ORDER BY extname")
            return database, user, dict(cursor.fetchall())
