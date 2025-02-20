from ollama import chat
from ollama import ChatResponse
import re


class Player:
    def __init__(self, modelo, chat=[]):
        self.modelo = modelo
        self.chat = chat
        self.coins = 2
        self.cards = []

    def borrar_pensamiento(self, texto):
        patron = r'<think>.*?</think>'
        texto_limpio = re.sub(patron, '', texto, flags=re.DOTALL)
        return texto_limpio

    def limpiar_respuesta(self, texto):
        texto_limpio = self.borrar_pensamiento(texto)
        return f"{str(self)}: {texto_limpio.strip()}"

    def actualizar_chat(self, texto, sender):
        self.chat.append({'role': sender, 'content': texto})

    def generar_respuesta(self):
        response: ChatResponse = chat(model=self.modelo, messages=self.chat)
        return self.limpiar_respuesta(response.message.content)

    def gain_coins(self, amount):
        self.coins += amount

    def lose_coins(self, amount):
        self.coins -= amount

    def __str__(self):
        return f'{self.modelo}'
