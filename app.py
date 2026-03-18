import matplotlib
matplotlib.use("Agg")

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Job Trends Analyzer", layout="wide")

st.title("Job Trends Analyzer")

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
# FILTROS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    search = st.text_input("Buscar (python, data, ai...)")

with col2:
    category = st.selectbox(
        "Categoria",
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
# METRICAS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Ofertas", len(filtered_df))
col2.metric("Empresas", filtered_df["company_name"].nunique())
col3.metric("Ubicaciones", filtered_df["candidate_required_location"].nunique())

# -------------------------
# RESULTADOS
# -------------------------
if filtered_df.empty:
    st.warning("No hay resultados")
else:
    col1, col2 = st.columns(2)

    # -------------------------
    # GRAFICO EMPRESAS
    # -------------------------
    with col1:
        st.subheader("Top empresas")
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        filtered_df["company_name"].value_counts().head(10).plot(kind="bar", ax=ax1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)

    # -------------------------
    # GRAFICO UBICACIONES
    # -------------------------
    with col2:
        st.subheader("Ubicaciones")
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        filtered_df["candidate_required_location"].value_counts().head(10).plot(kind="barh", ax=ax2)
        plt.tight_layout()
        st.pyplot(fig2)

    # -------------------------
    # SKILLS AUTOMATICAS
    # -------------------------
    st.subheader("Top tecnologias")

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

    fig3, ax3 = plt.subplots(figsize=(5, 3))
    skills_df.head(8).plot(kind="barh", x="skill", y="count", ax=ax3)
    ax3.set_title("Top tecnologias", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig3)

    # -------------------------
    # TABLA
    # -------------------------
    st.subheader("Ofertas")

    st.dataframe(
        filtered_df[[
            "title",
            "company_name",
            "candidate_required_location"
        ]].head(20)
    )
