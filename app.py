"""Primera herramienta de diagnóstico de datos para MyR Route Optimizer."""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MyR | Calidad de datos", page_icon="📍", layout="wide")
st.title("MyR Route Optimizer")
st.caption("Etapa inicial · Diagnóstico de pedidos")
st.info("Prototipo en construcción. Los resultados de esta pantalla no son rutas optimizadas.")
st.write("Depósito de referencia: MyR Operador Logístico · -12.0695081, -76.9943621")
with st.expander("Estado de la conexión local"):
    st.caption("La conexión usa credenciales privadas configuradas en secrets.toml.")
    if st.button("Comprobar conexión"):
        try:
            from db import comprobar_conexion
            database, user, extensions = comprobar_conexion(st.secrets['postgres'])
            st.success(f"Conectado a {database} como {user}.")
            for name in ('postgis', 'pgrouting'):
                st.write(f"{name}: {extensions.get(name, 'no habilitada en esta base')}")
        except Exception:
            st.error("No fue posible conectar. Revisa la configuración privada y que PostgreSQL esté activo.")
file = st.file_uploader("Selecciona un CSV de pedidos", type="csv")
if file is not None:
    try:
        df = pd.read_csv(file)
        required = ["ID_Pedido", "Latitud", "Longitud", "Volumen_Carga_kg", "Ventana_Horaria", "Tiempo_Servicio_min"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            st.error("Faltan columnas obligatorias: " + ", ".join(missing))
        else:
            issues = pd.Series("", index=df.index, dtype="object")
            def mark(mask, message):
                issues.loc[mask.fillna(False)] += message + "; "
            mark(df['ID_Pedido'].isna() | df['ID_Pedido'].duplicated(keep=False), 'ID vacío o duplicado')
            lat = pd.to_numeric(df['Latitud'], errors='coerce')
            lon = pd.to_numeric(df['Longitud'], errors='coerce')
            mark(~lat.between(-13, -11) | ~lon.between(-78, -76), 'Coordenadas inválidas o fuera del ámbito')
            weight = pd.to_numeric(df['Volumen_Carga_kg'], errors='coerce')
            mark(weight.isna() | (weight <= 0) | (weight > 800), 'Peso inválido o mayor a 800 kg')
            service = pd.to_numeric(df['Tiempo_Servicio_min'], errors='coerce')
            mark(service.isna() | (service < 0), 'Tiempo de servicio inválido')
            windows = df['Ventana_Horaria'].fillna('').astype(str)
            parts = windows.str.extract(r'^\s*(\d{2}):(\d{2})\s*-\s*(\d{2}):(\d{2})\s*$').apply(pd.to_numeric, errors='coerce')
            start = parts[0]*60+parts[1]; end = parts[2]*60+parts[3]
            mark(parts.isna().any(axis=1) | (parts[0]>23) | (parts[2]>23) | (parts[1]>59) | (parts[3]>59) | (start>=end), 'Ventana horaria inválida')
            valid = issues.eq('')
            a,b,c=st.columns(3)
            a.metric('Registros',len(df)); b.metric('Válidos',int(valid.sum())); c.metric('Rechazados',int((~valid).sum()))
            result = pd.DataFrame({'fila_archivo': df.index+2, 'estado': valid.map({True:'Válido',False:'Rechazado'}), 'motivos':issues.str.rstrip('; ')})
            st.dataframe(result, hide_index=True, use_container_width=True)
            st.download_button('Descargar diagnóstico sin datos personales', result.to_csv(index=False).encode('utf-8-sig'), 'diagnostico.csv', 'text/csv')
    except Exception as exc:
        st.error(f'No se pudo leer el archivo: {exc}')
