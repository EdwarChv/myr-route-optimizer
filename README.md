# MyR Route Optimizer

Prototipo académico en construcción. El repositorio público no contiene datos de clientes ni contraseñas. La pantalla actual realiza diagnóstico de calidad, todavía no genera rutas ni implementa autenticación.

## Inicio local

En PowerShell, desde esta carpeta: `.\iniciar_local.ps1`. La credencial local se almacena cifrada para el usuario de Windows en `.secrets`, que está excluido de Git. Esta pantalla es local y aún no incluye login de aplicación; no publicarla todavía.

La base PostgreSQL debe ser una base dedicada. `sql/001_schema.sql` crea las extensiones, tablas iniciales, depósito y 15 vehículos de 800 kg. No ejecutarlo en una base compartida sin revisar permisos. Guardar credenciales en `.streamlit/secrets.toml`, nunca en Git.

La base local `myr_tesis` se creó y se verificó con PostGIS 3.4.2, pgRouting 3.6.2, seis tablas, un depósito y 15 vehículos. La cuenta local `myr_app` fue probada desde Streamlit y tiene permisos de lectura sobre depósito y vehículos. El procesamiento de cargas y las demás funciones aún no están implementados; cualquier permiso adicional se evaluará para esas funciones.

La aplicación pública tendrá autenticación y datos sintéticos antes de publicarse. No publicar `secrets.toml`, datos de clientes ni contraseñas.

