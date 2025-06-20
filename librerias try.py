import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize

# Prueba con una frase simple
text = "Hola, ¿cómo estás?"
tokens = word_tokenize(text)
print(tokens)  # Debería mostrar los tokens de la frase