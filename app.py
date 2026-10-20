
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard de Accidentes de Tránsito",
    page_icon="🚗",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    df = pd.read_csv('accidentes_transito_limpio.csv')
    return df

df = cargar_datos()

st.title("🚗 Dashboard de Análisis de Accidentes de Tránsito")
st.markdown("""
Esta aplicación interactiva permite consultar los indicadores clave y la distribución de 
accidentes viales según filtros geográficos, causas principales, franjas horarias y sexo del conductor.
""")

st.sidebar.header("Filtros de Búsqueda")

deptos_disponibles = ['Todos'] + list(df['departamento'].unique())
depto_seleccionado = st.sidebar.selectbox("Selecciona un Departamento:", deptos_disponibles)

vehiculos_disponibles = ['Todos'] + list(df['tipo_vehiculo'].unique())
vehiculo_seleccionado = st.sidebar.selectbox("Selecciona Tipo de Vehículo:", vehiculos_disponibles)

df_filtrado = df.copy()

if depto_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['departamento'] == depto_seleccionado]

if vehiculo_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['tipo_vehiculo'] == vehiculo_seleccionado]

st.sidebar.markdown("---")
st.sidebar.write(f"**Registros filtrados:** {len(df_filtrado)} de {len(df)}")

col1, col2, col3, col4 = st.columns(4)

total_accidentes = len(df_filtrado)
total_lesionados = df_filtrado['lesionados'].sum()
total_fallecidos = df_filtrado['fallecidos'].sum()
total_victimas = df_filtrado['total_victimas'].sum()

col1.metric("Total de Accidentes", total_accidentes)
col2.metric("Total Lesionados", total_lesionados)
col3.metric("Total Fallecidos", total_fallecidos)
col4.metric("Total Víctimas", total_victimas)

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Causa de los accidentes de transito")
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    causas_count = df_filtrado['causa_principal'].value_counts()
    sns.barplot(x=causas_count.values, y=causas_count.index, hue=causas_count.index, palette="Blues_r", legend=False, ax=ax1)
    ax1.set_xlabel("Cantidad de Accidentes")
    ax1.set_ylabel("Causa Principal")
    st.pyplot(fig1)

with col_right:
    st.subheader("2. Accidentes por franja horaria")
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    horario_order = ['Madrugada', 'Mañana', 'Tarde', 'Noche']
    sns.countplot(data=df_filtrado, x='rango_horario', order=horario_order, hue='rango_horario', palette="Purples_r", legend=False, ax=ax2)
    ax2.set_xlabel("Franja Horaria")
    ax2.set_ylabel("Cantidad de Accidentes")
    st.pyplot(fig2)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("3. Fallecidos por tipo de vehiculo")
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    vehiculo_fallecidos = df_filtrado.groupby('tipo_vehiculo')['fallecidos'].sum().reset_index().sort_values(by='fallecidos', ascending=False)
    sns.barplot(data=vehiculo_fallecidos, x='tipo_vehiculo', y='fallecidos', hue='tipo_vehiculo', palette="Reds_r", legend=False, ax=ax3)
    ax3.set_xlabel("Tipo de Vehículo")
    ax3.set_ylabel("Total de Fallecidos")
    st.pyplot(fig3)

with col_right2:
    st.subheader("4. victimas por sexo del conductor")
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sexo_victimas = df_filtrado.groupby('sexo_conductor')['total_victimas'].sum()
    if len(sexo_victimas) > 0 and sexo_victimas.sum() > 0:
        ax4.pie(
            sexo_victimas.values, 
            labels=sexo_victimas.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=['#5B9BD5', '#ED7D31']
        )
    else:
        ax4.text(0.5, 0.5, "Sin datos para el filtro seleccionado", ha='center', va='center')
    st.pyplot(fig4)

st.markdown("---")

st.subheader("Muestra de Datos Filtrados")
st.dataframe(df_filtrado[['id_accidente', 'fecha', 'departamento', 'causa_principal', 'tipo_vehiculo', 'sexo_conductor', 'lesionados', 'fallecidos', 'total_victimas']].head(10))
