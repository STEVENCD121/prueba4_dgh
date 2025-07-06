
import os
import pandas as pd
import numpy as np
import streamlit as st

# Cargar el archivo CSV
df = pd.read_csv("Parametros.csv")

# Título de la aplicación
st.title("Consultas para DGH")

Parametros_1 = pd.DataFrame(df, columns=[
    'Libro_Año', 'Lote', 'Tip_HC', 'RD a Dic_(Año)', 'P1_(Año-1)', 'P1_(Año)', '2P_(Año)', '3P_(Año)',
    'Prod_(Año)', 'Acum_Prod_(Año)', 'Forec_(Año+1)', 'InSitu_2P', '3P+2C_(Año)', 'IMR'
])

# Conversión a valores numéricos
columnas_a_convertir = [
    'RD a Dic_(Año)', 'P1_(Año-1)', 'P1_(Año)', '2P_(Año)', '3P_(Año)',
    'Prod_(Año)', 'Acum_Prod_(Año)', 'Forec_(Año+1)', 'InSitu_2P', '3P+2C_(Año)'
]

for col in columnas_a_convertir:
    Parametros_1[col] = pd.to_numeric(Parametros_1[col], errors='coerce')

# Eliminar filas con valores nulos en columnas clave para evitar errores
Parametros_1.dropna(subset=['P1_(Año-1)', 'P1_(Año)', 'Prod_(Año)', '3P_(Año)', 'RD a Dic_(Año)', 
                            'Forec_(Año+1)', '3P+2C_(Año)', 'Acum_Prod_(Año)', 'InSitu_2P', '2P_(Año)'], inplace=True)

# Cálculos de los indicadores
Parametros_1['IMR'] = ((Parametros_1['P1_(Año)'] - Parametros_1['P1_(Año-1)']) / Parametros_1['P1_(Año-1)']) * 100
Parametros_1['IRR'] = (Parametros_1['P1_(Año)'] - Parametros_1['P1_(Año-1)'] + Parametros_1['Prod_(Año)']) / Parametros_1['Prod_(Año)']
Parametros_1['ICR'] = (Parametros_1['P1_(Año)'] / Parametros_1['3P_(Año)']) * 100
Parametros_1['IDR'] = (Parametros_1['RD a Dic_(Año)'] / Parametros_1['P1_(Año)']) * 100
Parametros_1['IAR'] = Parametros_1['P1_(Año)'] / Parametros_1['Forec_(Año+1)']
Parametros_1['IARrc'] = Parametros_1['3P+2C_(Año)'] / Parametros_1['Forec_(Año+1)']
Parametros_1['FRact'] = (Parametros_1['Acum_Prod_(Año)'] / Parametros_1['InSitu_2P']) * 100
Parametros_1['FRf'] = ((Parametros_1['Acum_Prod_(Año)'] + Parametros_1['2P_(Año)']) / Parametros_1['InSitu_2P']) * 100

# Inputs de usuario
año = st.number_input("¿Qué Año de Libro necesitas buscar?", step=1, format="%d")
lote = st.text_input("¿Qué Lote necesitas buscar?")

# Filtrado
df_filtrado = Parametros_1[(Parametros_1['Libro_Año'] == int(año)) & (Parametros_1['Lote'] == lote)]

# Columnas a mostrar
columnas_originales = [
    'RD a Dic_(Año)', 'P1_(Año-1)', 'P1_(Año)', '2P_(Año)', '3P_(Año)',
    'Prod_(Año)', 'Acum_Prod_(Año)', 'Forec_(Año+1)', 'InSitu_2P', '3P+2C_(Año)'
]

columnas_mostrar = [
    f'RD_Dic ({año})', f'P1({año-1})', f'P1({año})', f'2P({año})', f'3P({año})',
    f'Prod({año})', f'Acum Prod({año})', f'Forec({año+1})', 'InSitu 2P', f'3P + 2C({año})'
]

columnas_tabla2 = ['IMR', 'IRR', 'ICR', 'IDR', 'IAR', 'IARrc', 'FRact', 'FRf']

# Mostrar resultados solo si se ingresaron datos
if not df_filtrado.empty:
    tabla1 = df_filtrado[columnas_originales].copy()
    tabla1.columns = columnas_mostrar
    tabla2 = df_filtrado[columnas_tabla2].round(2)

    st.markdown(f"### 📊 Cifras al 31 de Diciembre de {año}")
    st.markdown(f"**Lote:** {lote}")

    st.write("#### Tabla 1: Valores Originales")
    st.dataframe(tabla1)

    st.write("#### Tabla 2: Indicadores Calculados")
    st.dataframe(tabla2)
else:
    st.warning("⚠️ No se encontraron datos para el año y lote ingresados.")
