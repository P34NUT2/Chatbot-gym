import streamlit as st
from chatbot import respuesta, predict_class, gym_help
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


####################################################################################
######parte del front

st.set_page_config(
    page_title="Chatbot GYM",  # Título de la pestaña
    page_icon="💪",           # Emoji o ruta al favicon
    layout="wide",            # Diseño: "wide" (amplio) o "centered" (centrado)
    initial_sidebar_state="expanded",  # Estado inicial del menú lateral
)
st.title("Chatbot_GYM")
import streamlit as st

# Crear un menú deslizante en la barra lateral
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["Inicio", "Chatbot", "Rutinas"]
)

# Funcionalidades del menú
if opcion == "Inicio":
    st.title("Bienvenido a Chatbot Gym")
    st.write("Este chatbot te ayudará a encontrar ejercicios, planificar entrenamientos y resolver tus dudas sobre fitness.")
    st.write("Ademas gracias a nuestra IA te vamos a poder dar las rutinas mas eficientes segun lo que busques")
    st.write("Selecciona una opción del menú lateral para comenzar.")

elif opcion == "Chatbot":
    st.title("Chatbot Interactivo")
    st.write("Aquí puedes interactuar con el chatbot.")

    # Inicializar historial de mensajes y estado del primer mensaje
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "first_message" not in st.session_state:
        st.session_state.first_message = True

    # Mostrar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Enviar mensaje inicial del bot (si es la primera vez)
    if st.session_state.first_message:
        with st.chat_message("assistant"):
            st.markdown("Hola, ¿cómo estás?")
        st.session_state.messages.append({"role": "assistant", "content": "Hola, ¿cómo estás?"})
        st.session_state.first_message = False

    # Capturar mensaje del usuario y agregarlo al historial
    if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Respuesta del bot (aquí puedes agregar lógica personalizada)
        message_user = prompt
        tag = predict_class(prompt)
        res = respuesta(message_user)
    ###########################################
        if tag == "ayuda_ejercicio":
            st.write("para eso accede a la ventana de rutinas en el side bar porfa nuestra IA te va decir cual es la mejor")
    #####################
        else:
            #response = f"Entendido: {prompt}"
            with st.chat_message("assistant"):
                #st.markdown(response)
                st.markdown(res)
            #st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.messages.append({"role": "assistant", "content": res})
        

###############################ejercicios
elif opcion == "Rutinas":
    st.title("Rutinas")
    st.write("Selecciona un grupo muscular y un equipo para obtener recomendaciones.")

    # Entrada del usuario
    grupo_muscular = st.selectbox("Grupo muscular:", options=list(muscle_ids.keys()))
    equipo = st.selectbox("Equipo:", options=list(equipment_ids.keys()))

    # Mostrar resultados cuando ambos valores están seleccionados
    if grupo_muscular and equipo:
        # Obtener IDs correspondientes
        mgp_id = muscle_ids[grupo_muscular]
        eqp_id = equipment_ids[equipo]
        
        # Llamar a la función y obtener resultados
        eficiencia, ejercicios_similares = predecir_eficiencia(mgp_id, eqp_id)
        
        # Mostrar resultados
        st.subheader("Resultados")
        st.write(f"Eficiencia del ejercicio: **{eficiencia}**")
        st.write("Ejercicios similares:")
        st.dataframe(ejercicios_similares)

    # Mensaje para el caso donde no se seleccionan valores
    else:
        st.info("Selecciona tanto un grupo muscular como un equipo para ver los resultados.")


###############################################


