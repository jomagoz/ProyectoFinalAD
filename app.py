
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

#Creamos datos sintéticos realistas
np.random.seed(42)
fechas = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
n_productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Auriculares']
regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']

#Generamos el DataSet
data = []
for fecha in fechas:
    for _ in range(np.random.poisson(10)):   #10 Ventas promedio por día
        data.append({
            'fecha': fecha,
            'producto': np.random.choice(n_productos),
            'region': np.random.choice(regiones),
            'cantidad': np.random.randint(1, 6),
            'precio_unitario': np.random.uniform(50, 1500),
            'vendedor': f'Vendedor_{np.random.randint(1, 21)}'
        })

df = pd.DataFrame(data)
#print(df)
df['venta_total'] = df['cantidad'] * df['precio_unitario']
#print(df)
#print("Shape del DataSet:", df.shape)
#print("\Primeras filas:")
#print(df.head())
#print("\nInformación general:")
#print(df.info())
#print("\nestadísticas descriptivas")
#print(df.describe())

#1. Ventas por Mes
#def graficar_ventas(df):
df_monthly = df.groupby(df['fecha'].dt.to_period('M'))['venta_total'].sum().reset_index()
df_monthly['fecha'] = df_monthly['fecha'].astype(str)
#print(df_monthly)

fig_monthly = px.line(df_monthly, x='fecha', y='venta_total',
                      title='Tendencia de Ventas Mensuales',
                      labels={'venta_total': 'Ventas ($)', 'fecha': 'Mes'})
fig_monthly.update_traces(line=dict(width=3))
#fig_monthly.show()

#import app
#import importlib
#importlib.reload(app)
#app.graficar_ventas(df)

#2. Top productos
#def graficar_top_productos(df):
df_productos = df.groupby('producto')['venta_total'].sum().sort_values(ascending=True)
fig_productos = px.bar(x=df_productos.values, y=df_productos.index,
                       orientation='h', title='Ventas por Producto',
                       labels={'x': 'Ventas Totales ($)', 'y': 'Producto'})
#fig_productos.show()

#app.graficar_top_productos(df)

#3. Análisis Geografico
#def graficar_analisis_geografico(df):
df_regiones = df.groupby('region')['venta_total'].sum().reset_index()
fig_regiones = px.pie(df_regiones, values='venta_total', names='region',
                      title='Distribución de Ventas por Región',
                      labels={'venta_total': 'Ventas Totales ($)'})
#fig_regiones.show()

#app.graficar_analisis_geografico(df)

# 4. Correlación entre variables
#def graficar_correlacion_variables(df):
df_corr = df[['cantidad', 'precio_unitario', 'venta_total']].corr()
fig_heatmap = px.imshow(df_corr, text_auto=True, aspect="auto",
                        title='Correlación entre Variables',
                        labels=dict(x="Variables", y="Variables", color="Correlación"))
#fig_heatmap.show()

#app.graficar_correlacion_variables(df)

#5. Distribución de Ventas
#def graficar_distribucion_ventas(df):
fig_dist = px.histogram(df, x='venta_total', nbins=50,
                        title='Distribución de Ventas Individuales')
fig_dist.update_layout(bargap=0.2)
#fig_dist.show()

#app.graficar_distribucion_ventas(df)

# configuración de la página
st.set_page_config(page_title="Dashboard de Ventas",
                   page_icon=":bar_chart:", layout="wide")

st.title("Dashboard de Análisis de Ventas")
st.markdown("---")

#SiderBar para filtros
st.sidebar.header("Filtros")
productos_seleccionados = st.sidebar.multiselect(
    "Selecciona Productos:",
    options=df['producto'].unique(),
    default=df['producto'].unique(),
)

regiones_seleccionadas = st.sidebar.multiselect(
    "Selecciona Regiones:",
    options=df['region'].unique(),
    default=df['region'].unique(),
)

#Filtrar los datos basado en la selección
df_filtered = df[
    (df['producto'].isin(productos_seleccionados)) &
    (df['region'].isin(regiones_seleccionadas))
]

#Métricas principales
col1, col2, col3, col4 = st.columns(4)
with col1:
  st.metric("Ventas Totales", f"${df_filtered['venta_total'].sum():,.0f}")
with col2:
  st.metric("Promedio por Venta", f"${df_filtered['venta_total'].mean():.0f}")
with col3:
    st.metric("Número de Ventas", f"{len(df_filtered):,}")
with col4:
    crecimiento = ((df_filtered[df_filtered['fecha'] >= '2024-01-01']['venta_total'].sum() /
                    df_filtered[df_filtered['fecha'] < '2024-01-01']['venta_total'].sum()) - 1) * 100
    st.metric("Crecimiento de Ventas 2024", f"{crecimiento:.1f}%")

#Layout con dos columnas
col1, col2 = st.columns(2)
with col1:
  st.plotly_chart(fig_monthly, use_container_width=True)
  st.markdown("---")
  st.markdown("✅ **Conclusión**: La tendencia mensual de ventas permite identificar los periodos de mayor y menor actividad comercial. Esta información es clave para planificar campañas, promociones o inventarios estratégicamente.")
  st.plotly_chart(fig_productos, use_container_width=True)
  st.markdown("---")
  st.markdown("✅ **Conclusión**: El análisis por producto muestra claramente cuáles son los artículos más rentables. Los productos con mayor volumen de ventas pueden representar oportunidades de expansión o especialización comercial.")

with col2:
  st.plotly_chart(fig_regiones, use_container_width=True)
  st.markdown("---")
  st.markdown("✅ **Conclusión**: La distribución geográfica revela qué regiones concentran mayor facturación. Esto ayuda a focalizar esfuerzos logísticos, comerciales y de atención al cliente en zonas clave.")
  st.plotly_chart(fig_heatmap, use_container_width=True)
  st.markdown("---")
  st.markdown("✅ **Conclusión**: La matriz de correlación indica que existe una relación fuerte entre el total de venta y la cantidad, como es lógico. Esto valida la estructura del modelo de ventas y permite detectar posibles patrones de compra.")

#Gráfico completo en la parte inferior
st.plotly_chart(fig_dist, use_container_width=True)
st.markdown("---")
st.markdown("✅ **Conclusión**: La distribución de ventas individuales muestra cómo se comporta el valor de cada transacción. Si la mayoría de las ventas están concentradas en un rango bajo o medio, puede considerarse una estrategia de diversificación de precios.")
