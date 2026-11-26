# MyR Route Optimizer

Prototipo académico en construcción. El repositorio público no contiene datos de clientes ni contraseñas. La pantalla actual realiza diagnóstico de calidad, todavía no genera rutas ni implementa autenticación.

## Inicio local

En PowerShell, desde esta carpeta: `.\.venv\Scripts\python.exe -m streamlit run app.py`.

La base PostgreSQL debe ser una base dedicada. `sql/001_schema.sql` crea las extensiones, tablas iniciales, depósito y 15 vehículos de 800 kg. No ejecutarlo en una base compartida sin revisar permisos. Guardar credenciales en `.streamlit/secrets.toml`, nunca en Git.

La base local `myr_tesis` se creó y se verificó con PostGIS 3.4.2, pgRouting 3.6.2, seis tablas, un depósito y 15 vehículos. Se probó la conexión de solo lectura desde Streamlit con una credencial existente autorizada para la prueba; no se configuró como acceso permanente ni se concedieron permisos sobre tablas de tesis. Para operar con datos se deberá crear una cuenta propia de aplicación y configurar sus permisos y credenciales.

La aplicación pública tendrá autenticación y datos sintéticos antes de publicarse. No publicar `secrets.toml`, datos de clientes ni contraseñas.

