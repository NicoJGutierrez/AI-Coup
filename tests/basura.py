from ollama import chat
from ollama import ChatResponse

mess = [{
    'role': 'user',
    'content': 'I had a great day today!'
}]

response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=mess)
print(response.message.content)

mess = [
    {
        'role': 'user',
        'content': 'I had a great day today!'
    },
    response.message,
    {
        'role': 'user',
        'content': 'Yeah! I really loved it!'
    },
]

response: ChatResponse = chat(model='deepseek-r1:1.5b', messages=mess)
print(response.message.content)
