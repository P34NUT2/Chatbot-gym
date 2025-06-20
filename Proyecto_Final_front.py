import streamlit as st
import chatbot as CHAT

st.title("Chatbot_GYM")

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
'''if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Respuesta del bot (aquí puedes agregar lógica personalizada)
    
    #response = f"Entendido: {prompt}"
    with st.chat_message("assistant"):
        #st.markdown(response)
        st.markdown(prompt)
    #st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.messages.append({"role": "assistant", "content": prompt})'''

if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Variables para datos adicionales
    grupo_muscular = st.session_state.get("grupo_muscular", None)
    equipo = st.session_state.get("equipo", None)

    # Llamar a la función de respuesta
    res, follow_up = CHAT.respuesta(prompt, grupo_muscular, equipo)

    if follow_up:
        # Si el backend solicita más información
        if "grupo_muscular" in follow_up:
            grupo_muscular = st.text_input("Grupo muscular (Ejemplo: Pecho, Espalda, Pierna):")
            st.session_state.grupo_muscular = grupo_muscular
        if "equipo" in follow_up:
            equipo = st.text_input("Equipo de ejercicio (Ejemplo: Mancuerna, Barra):")
            st.session_state.equipo = equipo
    else:
        # Si ya se completó la interacción
        with st.chat_message("assistant"):
            st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

