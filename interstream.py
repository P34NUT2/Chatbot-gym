import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Dataset simulado para el ejemplo
data = {
    "Exercise_Name": ["Squat", "Deadlift", "Bench Press", "Pull-Up", "Plank"],
    "muscle_gp": ["Quadriceps", "Hamstrings", "Chest", "Lats", "Abdominals"],
    "Equipment": ["Barbell", "Barbell", "Barbell", "Body Only", "Body Only"],
    "Rating": [95, 93, 90, 85, 83]
}
df = pd.DataFrame(data)

# Diccionarios de mapeo para equipment y muscle_gp
equipment_ids = {
    "Dumbbell": 1, "Barbell": 2, "Body Only": 3, "Cable": 4, "Other": 5, 
    "Machine": 6, "Kettlebells": 7, "E-Z Curl Bar": 8, "Bands": 9, 
    "Cables": 10, "Weight Bench": 11, "Exercise Ball": 12, "Medicine Ball": 13, 
    "Dumbbells": 14
}

muscle_ids = {
    "Quadriceps": 1, "Shoulders": 2, "Abdominals": 3, "Chest": 4, "Triceps": 5, 
    "Biceps": 6, "Hamstrings": 7, "Forearms": 8, "Middle Back": 9, "Lats": 10, 
    "Lower Back": 11, "Glutes": 12, "Traps": 13, "Calves": 14, "Abductors": 15, 
    "Adductors": 16, "Neck": 17
}

# Agregar columnas con IDs al DataFrame
df["mgp_id"] = df["muscle_gp"].map(muscle_ids)
df["eqp_id"] = df["Equipment"].map(equipment_ids)

X = df[["mgp_id", "eqp_id"]].to_numpy()
y = df["Rating"].to_numpy()

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

def predecir_eficiencia(mgp_id, eqp_id):
    nv_ej = np.array([[mgp_id, eqp_id]])
    pred = knn.predict(nv_ej)
    distancias, indices = knn.kneighbors(nv_ej)

    if pred[0] >= 95:
        eficiencia = "Alta"
    elif pred[0] >= 90:
        eficiencia = "Media-Alta"
    elif pred[0] >= 85:
        eficiencia = "Media"
    else:
        eficiencia = "Baja"

    columnas_deseadas = ["Exercise_Name", "muscle_gp", "Equipment", "Rating"]
    ejercicios_similares = df.iloc[indices[0]][columnas_deseadas]
    return eficiencia, ejercicios_similares

# Interfaz con Streamlit
st.title("Chatbot Gym")
st.write("¡Bienvenido! Este chatbot te ayudará a encontrar ejercicios basados en tus preferencias.")

# Entrada del usuario
st.subheader("Consulta")
user_input = st.text_input(
    "Escribe el grupo muscular y el equipo que tienes disponibles separados por una coma (por ejemplo: 'Quadriceps, Barbell'):"
).strip()

if user_input:
    parts = user_input.split(",")
    if len(parts) == 2:
        muscle = parts[0].strip()
        equipment = parts[1].strip()

        if muscle in muscle_ids and equipment in equipment_ids:
            mgp_id = muscle_ids[muscle]
            eqp_id = equipment_ids[equipment]
            eficiencia, ejercicios_similares = predecir_eficiencia(mgp_id, eqp_id)

            st.subheader("Resultados")
            st.write(f"Eficiencia: **{eficiencia}**")
            st.write("Ejercicios similares:")
            st.dataframe(ejercicios_similares)
        else:
            st.error("No reconozco ese grupo muscular o equipo. Por favor, verifica tu entrada.")
    else:
        st.error("Por favor, proporciona el grupo muscular y el equipo separados por una coma.")
