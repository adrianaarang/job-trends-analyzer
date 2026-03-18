import matplotlib
matplotlib.use("Agg")

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests

st.title("📊 Job Trends Analyzer")

# -------------------------
# CARGAR DATOS
# -------------------------
url = "https://remotive.com/api/remote-jobs"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data["jobs"])
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()

# -------------------------
# LIMPIEZA
# -------------------------
for col in ["title", "company_name", "category", "candidate_required_location", "description"]:
    df[col] = df[col].fillna("").astype(str)

# -------------------------
# BUSCADOR
# -------------------------
search = st.text_input("🔍 Buscar (python, data, ai...)")

# -------------------------
# FILTRO CATEGORÍA
# -------------------------
category = st.selectbox(
    "📂 Categoría",
    ["Todas"] + sorted(df["category"].unique())
)

# -------------------------
# FILTRADO
# -------------------------
filtered_df = df.copy()

if category != "Todas":
    filtered_df = filtered_df[filtered_df["category"] == category]

if search:
    s = search.lower()
    filtered_df = filtered_df[
        filtered_df["title"].str.lower().str.contains(s) |
        filtered_df["company_name"].str.lower().str.contains(s) |
        filtered_df["description"].str.lower().str.contains(s)
    ]

# -------------------------
# RESULTADOS
# -------------------------
st.write("Ofertas encontradas:", len(filtered_df))

# -------------------------
# SI NO HAY DATOS
# -------------------------
if filtered_df.empty:
    st.warning("⚠️ No hay resultados")
else:
    # gráfico
    st.subheader("Top empresas")

    fig, ax = plt.subplots()
    filtered_df["company_name"].value_counts().head(10).plot(kind="bar", ax=ax)
    st.pyplot(fig)

    # tabla
    st.subheader("📋 Ofertas")
    st.dataframe(
        filtered_df[[
            "title",
            "company_name",
            "candidate_required_location"
        ]].head(20)
    )
