import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import requests


st.title("📊 Job Trends Analyzer")

url = "https://remotive.com/api/remote-jobs"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data["jobs"])

    st.write("Ofertas encontradas:", len(df))
    st.dataframe(df[["title", "company_name"]].head(20))

except Exception as e:
    st.error(f"Error cargando datos: {e}")
st.subheader("Top empresas")

fig, ax = plt.subplots()
df["company_name"].value_counts().head(10).plot(kind="bar", ax=ax)
st.pyplot(fig)
