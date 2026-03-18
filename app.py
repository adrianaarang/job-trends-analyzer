import matplotlib
matplotlib.use("Agg")

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
st.set_page_config(page_title="Job Trends Analyzer", layout="wide")

st.title(" Job Trends Analyzer (Real Data)")

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
    df = pd.DataFrame(data["jobs"])

# -------------------------
# LIMPIEZA 
# -------------------------
cols = ["title", "company_name", "category", "candidate_required_location", "description"]

for col in cols:
    df[col] = df[col].fillna("").astype(str)

# -------------------------
# FILTROS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    search = st.text_input("🔍 Buscar (python, java, ai, data...)")

with col2:
    category = st.selectbox(
        "📂 Categoría",
        ["Todas"] + sorted(df["category"].unique())
    )

# -------------------------
# FILTRADO
# -------------------------
filtered_df = df.copy()

# 1. categoría
if category != "Todas":
    filtered_df = filtered_df[filtered_df["category"] == category]

# 2. buscador
if search:
    search_lower = search.lower()

    filtered_df = filtered_df[
        filtered_df["title"].str.lower().str.contains(search_lower, regex=False) |
        filtered_df["company_name"].str.lower().str.contains(search_lower, regex=False) |
        filtered_df["candidate_required_location"].str.lower().str.contains(search_lower, regex=False) |
        filtered_df["description"].str.lower().str.contains(search_lower, regex=False)
    ]

# -------------------------
# ORDEN
# -------------------------
order = st.selectbox("Ordenar por", ["Ninguno", "Empresa (A-Z)", "Empresa (Z-A)"])

if order == "Empresa (A-Z)":
    filtered_df = filtered_df.sort_values("company_name")

elif order == "Empresa (Z-A)":
    filtered_df = filtered_df.sort_values("company_name", ascending=False)

# -------------------------
# MÉTRICAS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📌 Ofertas", len(filtered_df))
col2.metric("🏢 Empresas", filtered_df["company_name"].nunique())
col3.metric("🌍 Ubicaciones", filtered_df["candidate_required_location"].nunique())

# -------------------------
# SI NO HAY RESULTADOS
# -------------------------
if filtered_df.empty:
    st.warning("⚠️ No hay resultados con esos filtros")

# -------------------------
# GRÁFICOS
# -------------------------
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top empresas")
        fig1, ax1 = plt.subplots()
        filtered_df["company_name"].value_counts().head(10).plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("Top ubicaciones")
        fig2, ax2 = plt.subplots()
        filtered_df["candidate_required_location"].value_counts().head(10).plot(kind="barh", ax=ax2)
        st.pyplot(fig2)

# -------------------------
# TABLA FINAL
# -------------------------
st.subheader("📋 Ofertas de trabajo")

st.dataframe(
    filtered_df[[
        "title",
        "company_name",
        "candidate_required_location",
        "category"
    ]]
)

# -------------------------
# SKILLS DETECTADAS
# -------------------------
st.subheader("🛠️ Top tecnologías detectadas")

skills_list = [
    "python", "java", "javascript", "react", "node", "sql",
    "aws", "docker", "kubernetes", "html", "css",
    "machine learning", "ai", "data", "pandas"
]

text = filtered_df["description"].str.lower().str.cat(sep=" ")

skill_counts = {}

for skill in skills_list:
    skill_counts[skill] = text.count(skill)

skills_df = pd.DataFrame(
    skill_counts.items(),
    columns=["skill", "count"]
).sort_values(by="count", ascending=False)

# gráfico
fig, ax = plt.subplots()
skills_df.head(10).plot(kind="bar", x="skill", y="count", ax=ax)
st.pyplot(fig)
