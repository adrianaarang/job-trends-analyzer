import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("ggplot")

# cargar datos
df = pd.read_csv("jobs.csv")

# crear figura con 3 gráficos
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# -------------------------
# 1. Trabajos más demandados
# -------------------------
df["title"].value_counts().plot(kind="bar", ax=axs[0, 0])
axs[0, 0].set_title("Trabajos más demandados")
axs[0, 0].tick_params(axis='x', rotation=45)

# -------------------------
# 2. Salario medio
# -------------------------
df.groupby("title")["salary"].mean().sort_values().plot(kind="barh", ax=axs[0, 1])
axs[0, 1].set_title("Salario medio por puesto")

# -------------------------
# 3. Ofertas por ciudad
# -------------------------
df["location"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=axs[1, 0])
axs[1, 0].set_title("Ofertas por ciudad")
axs[1, 0].set_ylabel("")

# -------------------------
# 4. Skills más demandadas
# -------------------------
skills = df["skills"].str.split(";").explode()
skills.value_counts().head(10).plot(kind="bar", ax=axs[1, 1])
axs[1, 1].set_title("Top skills")

plt.tight_layout()
plt.show()