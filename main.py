# todo:
# - [ ] Crear repo en github
# - [ ] Limpiar las respuestas para que tengan menos \n
# - [ ] Poner los nombres al lado de lo que escriben
# - [ ] Hacerlos jugar coup

from ollama import chat
from ollama import ChatResponse
import re


def borrar_pensamiento(texto):
    # Expresión regular para encontrar todo lo que esté entre <think> y </think>
    patron = r'<think>.*?</think>'
    # Reemplazar lo encontrado con una cadena vacía
    texto_limpio = re.sub(patron, '', texto, flags=re.DOTALL)
    # Expresión regular para encontrar los <think> y </think> que no se cerraron
    patron = r'<think>.*?'
    # Reemplazar lo encontrado con una cadena vacía
    texto_limpio = re.sub(patron, '', texto_limpio, flags=re.DOTALL)
    return texto_limpio


print('gemma:')
print('I had a great day today!')
mess = [{
    'role': 'user',
    'content': 'I had a great day today!'
}]
mess2 = [{
    'role': 'assistant',
    'content': 'I had a great day today!'
}]


for i in range(5):
    response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=mess)
    print("dipsik:")
    print(borrar_pensamiento(response.message.content).strip())
    response_mess = response.message.content
    response_mess = borrar_pensamiento(response_mess)
    mess.append({'role': 'assistant', 'content': response_mess})
    mess2.append({'role': 'user', 'content': response_mess})

    response: ChatResponse = chat(model='gemma2:2b', messages=mess2)

    print("gemma:")
    print(borrar_pensamiento(response.message.content).strip())
    response_mess = response.message.content
    response_mess = borrar_pensamiento(response_mess)
    mess.append({'role': 'user', 'content': response_mess})
    mess2.append({'role': 'assistant', 'content': response_mess})
