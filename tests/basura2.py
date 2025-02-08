from ollama import chat
from ollama import ChatResponse
import re


def borrar_pensamiento(texto):
    # Expresión regular para encontrar todo lo que esté entre <think> y </think>
    patron = r'<think>.*?</think>'
    # Reemplazar lo encontrado con una cadena vacía
    texto_limpio = re.sub(patron, '', texto, flags=re.DOTALL)
    return texto_limpio


mess = [{
    'role': 'user',
    'content': 'Heads or tails?'
}]

response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=mess)
print(borrar_pensamiento(response.message.content))

mess = [
    {
        'role': 'user',
        'content': borrar_pensamiento(response.message.content),
    },
]

response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=mess)
print(borrar_pensamiento(response.message.content))
