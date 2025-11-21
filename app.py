import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px



import streamlit as st

st.set_page_config(
    page_title="Dashboard Seguimiento de pagos planes Postpagos", 
    layout="wide",
    # Añadir esto para quitar la barra lateral (si no la necesitas)
    initial_sidebar_state="collapsed" 
)

# ==============================
# HEADER CON COLOR ROJO - titulo
# ==============================
st.markdown(
    """
    <div style="background-color:#FF0000; padding:15px; border-radius:8px;">
        <h1 style="color:white; text-align:center;">📊 Dashboard Seguimiento de pagos – Planes postpago 2025</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# Función para cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_excel("con y sin Pago postpago.xlsx")
    # Normalizar nombres de sucursales
    df['Sucursal'] = df['Sucursal'].str.strip()
    return df

# Cargar datos
df = cargar_datos()


# === Menú lateral ===

from PIL import Image

# Cargar imagen usando ruta relativa
logo = Image.open("logo.png")

# Mostrar logo en el sidebar
st.sidebar.image(logo, use_container_width=True)



st.sidebar.title("📊 Filtros de información")


# --- Selección de sucursal ---
sucursales = sorted(df['Sucursal'].dropna().unique().tolist())
sucursales.insert(0, "Todas")

sucursales_seleccionadas = st.sidebar.multiselect(
    "Selecciona una o varias sucursales",
    sucursales,
    default=["Todas"]
)

# --- Selección de rol ---
roles = sorted(df['RolVendedor'].dropna().unique().tolist())
roles.insert(0, "Todas")

roles_seleccionadas = st.sidebar.multiselect(
    "Selecciona una o varios roles de vendedor",
    roles,
    default=["Todas"]
)

# --- Selección de mes o fecha de facturación ---
fechas = sorted(df['fecha_factura'].dropna().unique().tolist())
fechas.insert(0, "Todas")

fechas_seleccionadas = st.sidebar.multiselect(
    "Selecciona una o varios meses de facturación de NxtSoft",
    fechas,
    default=["Todas"]
)

# --- Selección de CFM ---
cfm = sorted(df['cfm_con_iva'].dropna().unique().tolist())
cfm.insert(0, "Todas")

cfm_seleccionadas = st.sidebar.multiselect(
    "Selecciona uno o varios CFM ",
    cfm,
    default=["Todas"]
)

# --- Selección de estado_pago ---
pago = sorted(df['estado_pago'].dropna().unique().tolist())
pago.insert(0, "Todas")

pago_seleccionadas = st.sidebar.multiselect(
    "Selecciona el estado de pago de los planes ",
    pago,
    default=["Todas"]
)
# === Filtrado de datos ===
df_filtrado = df.copy()

# Si se elige algo diferente a "Todas", filtramos
if "Todas" not in sucursales_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['Sucursal'].isin(sucursales_seleccionadas)]

# Si se elige algo diferente a "Todas", filtramos
if "Todas" not in roles_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['RolVendedor'].isin(roles_seleccionadas)]

if "Todas" not in fechas_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['fecha_factura'].isin(fechas_seleccionadas)]

if "Todas" not in cfm_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['cfm_con_iva'].isin(cfm_seleccionadas)]

if "Todas" not in pago_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['estado_pago'].isin(pago_seleccionadas)]




# ==============================
# 🔍 FILTRADO DE DATOS
# ==============================
df_filtrado = df.copy()

if "Todas" not in sucursales_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['Sucursal'].isin(sucursales_seleccionadas)]

if "Todas" not in roles_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['RolVendedor'].isin(roles_seleccionadas)]

if "Todas" not in fechas_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['fecha_factura'].isin(fechas_seleccionadas)]

if "Todas" not in cfm_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['cfm_con_iva'].isin(cfm_seleccionadas)]

if "Todas" not in pago_seleccionadas:
    df_filtrado = df_filtrado[df_filtrado['estado_pago'].isin(pago_seleccionadas)]

# ==============================
# 📊 AGRUPAR POR SUCURSAL (CONTEO)
# ==============================
df_agrupado = (
    df_filtrado
    .groupby('Sucursal', as_index=False)
    .size()  # Cuenta cantidad de filas
    .rename(columns={'size': 'Cantidad'})
    .sort_values('Cantidad', ascending=False)
)

import streamlit as st
import plotly.graph_objects as go

# Simulación de datos (usa tu DataFrame real)
cantidad = 120
total_cortes = 4500000
puntos = 320
total_lineas = 164
con_pago = 142
sin_pago = 22
porcentaje_pago = round((con_pago / total_lineas) * 100, 2)

# ==============================
# Diseño en dos columnas
# ==============================
# ==============================
# 📦 TARJETAS SUPERIORES (Resumen + Estado de Pago)
# ==============================

# Cálculos
cantidad = len(df_filtrado)
total_cortes = df_filtrado["total_cortes"].sum() if "total_cortes" in df_filtrado.columns else 0
puntos = df_filtrado["puntos"].sum() if "puntos" in df_filtrado.columns else 0
porcentaje_pago = 85  # ejemplo, puedes calcularlo con tus datos reales

# ===== CSS Personalizado =====
st.markdown("""
<style>
.card-box {
    background: #ffffff;
    border-radius: 15px;
    padding: 20px 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.card-title {
    font-size: 20px;
    font-weight: bold;
    color: #222;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
}
.metric {
    font-size: 18px;
    margin-bottom: 8px;
}
.metric b {
    font-size: 22px;
    color: #000;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔹 DISEÑO EN DOS COLUMNAS (LAS TARJETAS)
# ==============================
col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown('<div class="card-title">🧾 Resumen general</div>', unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados.")
    else:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric">📄 <b>{cantidad:,}</b><br>Cantidad</div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric">💵 <b>{total_cortes:,}</b><br>Total Cortes</div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric">⭐ <b>{puntos:,.1f}</b><br>Puntos</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
  
    st.markdown('<div class="card-title">📊 Estado de Pagos</div>', unsafe_allow_html=True)

    # ===== Gráfico tipo gauge circular =====
    n_segments = 20
    filled_segments = int((porcentaje_pago / 100) * n_segments)
    colors = ["#E93131" if i < filled_segments else "#E0E0E0" for i in range(n_segments)]

    fig = go.Figure(go.Pie(
        values=[1]*n_segments,
        hole=0.7,
        marker=dict(colors=colors, line=dict(color="white", width=2)),
        textinfo="none",
        sort=False
    ))

    fig.add_annotation(
        text=f"<b>{porcentaje_pago}%</b><br>Con Pago",
        font=dict(size=16, color="#333"),
        showarrow=False
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=150,
        width=150,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)




tab1, tab2, tab3, tab4, tab5 = st.tabs(['Gráfico', 'Tabla', 'Vendedor', 'Mes', 'Cortes'])

with tab1:
    # ==============================
    # 📈 GRÁFICO UNIFICADO DE CANTIDAD Y TOTAL (COP)
    # ==============================
    # Agrupar información
    df_agrupado = (
        df_filtrado.groupby("Sucursal", as_index=False)
        .agg(
            Cantidad=("total_cortes", "count"),
            Total_COP=("total_cortes", "sum")
        )
        .sort_values("Total_COP", ascending=False)
    )

    if df_agrupado.empty:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados.")
    else:
        fig = go.Figure()

        # 💰 Barras: Total en COP
        fig.add_trace(go.Bar(
            x=df_agrupado["Sucursal"],
            y=df_agrupado["Total_COP"],
            name="<b>💰 Total (COP)</b>",  # Negrilla en leyenda
            marker_color="rgba(255, 102, 102, 0.7)",
            text=[f"<b>${v:,.0f}</b>".replace(",", ".") for v in df_agrupado["Total_COP"]],  # Negrilla en valores
            textposition="outside",
            textfont=dict(size=16, color="black", family="Arial")
        ))

        # 📈 Línea: Cantidad de pagos
        fig.add_trace(go.Scatter(
            x=df_agrupado["Sucursal"],
            y=df_agrupado["Cantidad"],
            name="<b>📦 Cantidad de pagos</b>",  # Negrilla en leyenda
            mode="lines+markers+text",
            text=[f"<b>{int(v):,}</b>".replace(",", ".") for v in df_agrupado["Cantidad"]],  # Negrilla en valores
            textposition="top center",
            line=dict(color="rgba(255, 182, 193, 0.9)", width=3),
            marker=dict(size=12, color="rgba(139, 0, 0, 0.9)"),
            yaxis="y2"
        ))


        # 🧭 Configuración de diseño
        fig.update_layout(
            height=700,  # Más espacio vertical
            margin=dict(t=150, b=80),  # Márgenes superiores e inferiores
            title=dict(
                text="📈 Relación entre cantidad de pagos y total (COP) por sucursal</b>",
                font=dict(size=24, family="Arial Black", color="black")
            ),
            xaxis=dict(
                tickangle=-90,
                tickfont=dict(size=12, color="black", family="Arial Black")
            ),
            yaxis=dict(
                title=dict(text="💰 Total (COP)</b>", font=dict(size=14, family="Arial Black", color="black")),
                tickfont=dict(size=12, color="black", family="Arial Black")
            ),
            yaxis2=dict(
                title=dict(text="📦 Cantidad de pagos</b>", font=dict(size=12, family="Arial Black", color="black")),
                tickfont=dict(size=12, color="black", family="Arial Black"),
                overlaying="y",
                side="right"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=12, family="Arial Black", color="black")
            ),
            bargap=0.3,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        # Evitar que se recorten los textos
        fig.update_traces(cliponaxis=False)

        st.plotly_chart(fig, use_container_width=True)



with tab2:

    # ==============================
    # 🔍 Cuadro de búsqueda pequeño
    # ==============================
    col1, col2 = st.columns([1, 3])   # Ajusta los valores para hacerlo más pequeño o grande

    with col1:
        busqueda = st.text_input("🔍 Buscar:", "")

    df_resultado = df_filtrado.copy()

    if busqueda.strip() != "":
        texto = busqueda.lower()

        # Convertimos todas las columnas a texto
        df_str = df_filtrado.astype(str).apply(lambda col: col.str.lower())

        # Creamos una máscara para saber qué filas coinciden en cualquier columna
        mask = df_str.apply(lambda col: col.str.contains(texto, na=False)).any(axis=1)

        # Filtramos
        df_resultado = df_filtrado[mask]

    # ==============================
    # 📋 TABLA
    # ==============================
    st.subheader("📋 Datos filtrados")
    st.caption(f"Mostrando {len(df_resultado)} registros que coinciden con la búsqueda.")
    st.dataframe(df_resultado, use_container_width=True)





with tab3:

      # ==============================
    # 📋 TABLA DE RESULTADOS
    # ==============================
    st.subheader("⚖️ Barra de progreso y cantidad por vendedor")

# Agrupar datos reales por vendedor
    df_agrupado = (
    df_filtrado.groupby("NombreVendedor", as_index=False)
    .agg(Cantidad=("cfm_con_iva", "count"))  # Ajusta la columna según tu dataset
    .sort_values("Cantidad", ascending=False)
    )

    # Definir meta (puedes cambiarla o calcularla dinámicamente)
    meta = df_agrupado["Cantidad"].max()  # La meta será el máximo valor
    df_agrupado["Progreso"] = (df_agrupado["Cantidad"] / meta) * 100

    # ==============================
    # HTML + CSS para tabla con barra de progreso
    # ==============================
    st.markdown(
    """
    <style>
        .table-container {
            width: 100%;
            background: #1E1E2F;
            color: #fff;
            border-radius: 10px;
            padding: 15px;
            font-family: Arial, sans-serif;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
        }
        th {
            color: #bbb;
            font-size: 14px;
        }
        .progress-bar {
            background: #333;
            border-radius: 5px;
            overflow: hidden;
            height: 8px;
            width: 100%;
        }
        .progress {
            height: 100%;
            background: #FF0000; /* Rojo sólido */
        }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Renderizar tabla completa
    st.markdown('<div class="table-container"><table>', unsafe_allow_html=True)
    st.markdown('<tr><th>Vendedor</th><th>Cantidad</th><th>Progreso</th></tr>', unsafe_allow_html=True)

    for _, row in df_agrupado.iterrows():
        st.markdown(
        f"""
        <tr>
            <td>{row['NombreVendedor']}</td>
            <td>{row['Cantidad']}</td>
            <td>
                <div class="progress-bar">
                    <div class="progress" style="width:{row['Progreso']}%;"></div>
                </div>
                {row['Progreso']:.0f}%
            </td>
        </tr>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</table></div>', unsafe_allow_html=True)


with tab4:
   
    # ==============================
    # 📈 GRÁFICO UNIFICADO DE CANTIDAD Y TOTAL (COP) por mes
    # ==============================

    
    # Diccionario para convertir nombres de meses a número
    meses_dict = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }

    # Normalizar texto en la columna fecha_factura
    df_filtrado["fecha_factura"] = df_filtrado["fecha_factura"].str.lower().str.strip()

    # Crear columna Mes (número) usando el diccionario
    df_filtrado["Mes"] = df_filtrado["fecha_factura"].map(meses_dict)

    # Crear columna Mes_nombre (capitalizado)
    df_filtrado["Mes_nombre"] = df_filtrado["fecha_factura"].str.capitalize()

    # Eliminar filas donde Mes sea NaN (mes no reconocido)
    df_filtrado = df_filtrado.dropna(subset=["Mes"])


    # 4. Agrupar por mes
    df_agrupado = (
        df_filtrado.groupby(["Mes", "Mes_nombre"], as_index=False)
        .agg(
            Cantidad=("total_cortes", "count"),
            Total_COP=("total_cortes", "sum")
        )
        .sort_values("Mes")  # Orden cronológico
    )

    # ✅ Verificación antes de graficar
    if df_agrupado.empty:
        st.warning("⚠️ No hay datos que coincidan con los filtros seleccionados.")
        st.write("Revisa el formato de fecha en la columna 'fecha_factura'.")
    else:
        # ==============================
        # Gráfico
        # ==============================
        fig = go.Figure()

        # 💰 Barras: Total en COP
        fig.add_trace(go.Bar(
            x=df_agrupado["Mes_nombre"],
            y=df_agrupado["Total_COP"],
            name="<b>💰 Total (COP)</b>",
            marker_color="rgba(150, 150, 150, 0.7)",
            text=[f"<b>${v:,.0f}</b>".replace(",", ".") for v in df_agrupado["Total_COP"]],
            textposition="outside",
            textfont=dict(size=16, color="black", family="Arial")
        ))

        # 📈 Línea: Cantidad de pagos
        fig.add_trace(go.Scatter(
            x=df_agrupado["Mes_nombre"],
            y=df_agrupado["Cantidad"],
            name="<b>📦 Cantidad de pagos</b>",
            mode="lines+markers+text",
            text=[f"<b>{int(v):,}</b>".replace(",", ".") for v in df_agrupado["Cantidad"]],
            textposition="top center",
            line=dict(color="rgba(255, 102, 102, 0.7)", width=3),
            marker=dict(size=12, color="rgba(139, 0, 0, 0.9)"),
            yaxis="y2"
        ))

        # 🧭 Configuración de diseño
        fig.update_layout(
            height=700,
            margin=dict(t=150, b=80),
            title=dict(
                text="<b>📈 Relación entre cantidad de pagos y total (COP) por mes de facturación en nextSoft</b>",
                font=dict(size=24, family="Arial Black", color="black")
            ),
            xaxis=dict(
                tickangle=-90,
                tickfont=dict(size=12, color="black", family="Arial Black")
            ),
            yaxis=dict(
                title=dict(text="<b>💰 Total (COP)</b>", font=dict(size=14, family="Arial Black", color="black")),
                tickfont=dict(size=12, color="black", family="Arial Black")
            ),
            yaxis2=dict(
                title=dict(text="<b>📦 Cantidad de pagos</b>", font=dict(size=14, family="Arial Black", color="black")),
                tickfont=dict(size=12, color="black", family="Arial Black"),
                overlaying="y",
                side="right"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=12, family="Arial Black", color="black")
            ),
            bargap=0.3,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        # Evitar que se recorten los textos
        fig.update_traces(cliponaxis=False)

        st.plotly_chart(fig, use_container_width=True)



with tab5:


   # ==============================
    # 📊 ANÁLISIS DE PAGOS POR CORTE Y MES
    # ==============================

    if df_filtrado.empty:
        st.warning("⚠️ No hay datos que coincidan con los filtros para el análisis de cortes.")
    else:
        # ==============================
        # 1. Normalizar columna fecha_factura
        # ==============================
        meses_dict = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
            "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }

        df_filtrado["fecha_factura"] = df_filtrado["fecha_factura"].str.lower().str.strip()
        df_filtrado["Mes"] = df_filtrado["fecha_factura"].map(meses_dict)
        df_filtrado["Mes_nombre"] = df_filtrado["fecha_factura"].str.capitalize()

        # ==============================
        # 2. Filtrar solo pagos confirmados
        # ==============================
        df_pagos_filtrado = df_filtrado[df_filtrado["estado_pago"] == "Con Pago"].copy()

        # Identificar columnas de cortes
        columnas_corte = sorted([
            col for col in df_pagos_filtrado.columns
            if col.startswith("corte") and col != "total_cortes"
        ])

        # ==============================
        # 🔎 3. Buscador general de cortes (reemplaza multiselect)
        # ==============================

        busqueda_corte = st.text_input(
            "🔎 Buscar corte (general):",
            "",
            placeholder="Escribe para filtrar: ej. '3', 'cor', 'te4'..."
        )

        # Filtrar cortes según texto
        if busqueda_corte.strip() == "":
            cortes_seleccionados = columnas_corte
        else:
            cortes_seleccionados = [
                c for c in columnas_corte
                if busqueda_corte.lower() in c.lower()
            ]

        # Mostrar cortes filtrados
        st.write("Cortes filtrados:", ", ".join(cortes_seleccionados))

        # Convertir cortes a numérico
        for col in cortes_seleccionados:
            df_pagos_filtrado[col] = pd.to_numeric(df_pagos_filtrado[col], errors="coerce").fillna(0)

        # Filtro por año si existe
        if "anio" in df_pagos_filtrado.columns:
            anios = sorted(df_pagos_filtrado["anio"].dropna().unique())
            anio_seleccionado = st.selectbox("Selecciona el año:", options=anios)
            df_pagos_filtrado = df_pagos_filtrado[df_pagos_filtrado["anio"] == anio_seleccionado]

        # ==============================
        # 4. Calcular métricas por mes y corte
        # ==============================
        resultados = []
        for corte in cortes_seleccionados:
            df_corte = df_pagos_filtrado[df_pagos_filtrado[corte] > 0]

            resumen = df_corte.groupby(["Mes", "Mes_nombre"], as_index=False).agg(
                Cantidad=("numero_linea", "count"),
                Valor=("total_cortes", "sum")
            )
            resumen["Corte"] = corte.capitalize()

            resultados.append(resumen)

        # Unir todos los cortes
        if resultados:
            df_resumen = pd.concat(resultados, ignore_index=True)
        else:
            st.warning("⚠️ No hay cortes coincidentes con la búsqueda.")
            st.stop()

        df_resumen = df_resumen.sort_values(["Mes", "Corte"])

        # ==============================
        # 5. Tabla Resumen
        # ==============================
        st.subheader("📋 Detalle de Pagos por Corte y Mes")

        df_resumen["Valor (COP)"] = df_resumen["Valor"].apply(lambda x: f"$ {x:,.0f}".replace(",", "."))

        st.dataframe(
            df_resumen[["Mes_nombre", "Corte", "Cantidad", "Valor (COP)"]],
            use_container_width=True
        )

        # ==============================
        # 6. Gráfico — Cantidades
        # ==============================
        fig_cantidades = px.line(
            df_resumen,
            x="Mes_nombre",
            y="Cantidad",
            color="Corte",
            markers=True,
            title="📦 Cantidad de número_linea pagadas por Corte y Mes"
        )

        fig_cantidades.update_traces(
            mode="lines+markers+text",
            text=df_resumen["Cantidad"],
            textposition="top center"
        )

        fig_cantidades.update_layout(
            xaxis=dict(categoryorder="array", categoryarray=[
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ])
            
        )
        

        st.plotly_chart(fig_cantidades, use_container_width=True)
        
        # ==============================
        # 7. Gráfico — Valores COP
        # ==============================
        fig_valores = px.line(
            df_resumen,
            x="Mes_nombre",
            y="Valor",
            color="Corte",
            markers=True,
            title="💰 Valor total pagado por Corte y Mes (COP)"
        )

        fig_valores.update_traces(
            mode="lines+markers+text",
            text=[f"$ {v:,.0f}".replace(",", ".") for v in df_resumen["Valor"]],
            textposition="top center"
        )

        fig_valores.update_layout(
            xaxis=dict(categoryorder="array", categoryarray=[
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ])
        )

        st.plotly_chart(fig_valores, use_container_width=True)
