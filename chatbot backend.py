import random
import json
import pickle
import numpy as np
import pandas as pd

import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from sklearn.neighbors import KNeighborsClassifier

lemmatizer = WordNetLemmatizer()

# Cargar los archivos generados en el código anterior
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Cargar el dataset de ejercicios para la predicción de eficiencia
archivo = "gymdataset.csv"
df = pd.read_csv(archivo)

# Reemplazar valores nulos o vacíos
df["Equipment"] = df["Equipment"].fillna("Other").replace("", "Other")

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
#:)
# Preprocesamiento de datos
df["Rating"] = (df["Rating"] * 10).astype(int)
df["eqp_id"] = df["Equipment"].map(equipment_ids)
df["mgp_id"] = df["muscle_gp"].map(muscle_ids)

# Datos de entrada: [muscle_gp, equipment]
X = df[["mgp_id", "eqp_id"]].to_numpy()
y = df["Rating"].to_numpy()

# Crear el modelo k-NN con k=5
knn = KNeighborsClassifier(n_neighbors=5)

# Entrenar el modelo
knn.fit(X, y)

# Función para predecir la eficiencia del ejercicio
def predecir_eficiencia(mgp_id, eqp_id):
    nv_ej = np.array([[mgp_id, eqp_id]])
    pred = knn.predict(nv_ej)
    distancias, indices = knn.kneighbors(nv_ej)

    # Clasificar eficiencia
    if pred[0] >= 95:
        eficiencia = "alta"
    elif pred[0] < 95 and pred[0] >= 90:
        eficiencia = "media-alta"
    elif pred[0] < 90 and pred[0] >= 85:
        eficiencia = "media"
    elif pred[0] < 85 and pred[0] >= 83:
        eficiencia = "media-baja"
    else:
        eficiencia = "baja"

    # Mostrar los ejercicios similares
    columnas_deseadas = ["Exercise_Name", "muscle_gp", "Equipment", "Rating"]
    ejercicios_similares = df.iloc[indices[0]][columnas_deseadas]

    return eficiencia, ejercicios_similares

# Función para limpiar y lematizar la oración
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Convertir la oración a un vector de unos y ceros según si están presentes en los patrones
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predecir la categoría de la oración
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

# Obtener una respuesta basada en la categoría
def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Función que maneja la interacción del chatbot
def respuesta(message):
    ints = predict_class(message)
    res = get_response(ints, intents)

    if ints == "ayuda_ejercicio":
        # Solicitar grupo muscular y equipo de ejercicio
        res = "¿Qué grupo muscular deseas trabajar? (Ejemplo: Pecho, Espalda, Pierna)"
        grupo_muscular = input("Grupo muscular: ")  # El usuario ingresa grupo muscular
        res += f"\n¿Con qué equipo de ejercicio deseas entrenar? (Ejemplo: Mancuerna, Barra)"
        equipo = input("Equipo de ejercicio: ")  # El usuario ingresa equipo de ejercicio

        # Validar que el grupo muscular y el equipo estén en el diccionario
        if grupo_muscular not in muscle_ids or equipo not in equipment_ids:
            return "Lo siento, no puedo procesar esa combinación. Intenta nuevamente."
        
        # Obtener el id correspondiente
        mgp_id = muscle_ids[grupo_muscular]
        eqp_id = equipment_ids[equipo]

        # Predecir la eficiencia y recomendar ejercicios
        eficiencia, ejercicios_similares = predecir_eficiencia(mgp_id, eqp_id)
        res += f"\nEficiencia recomendada: {eficiencia}. Aquí tienes algunos ejercicios similares:\n{ejercicios_similares}"
    
    return res

# Bucle de interacción del chatbot
while True:
    message = input("Usuario: ")
    print("Chatbot:", respuesta(message))