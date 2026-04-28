import httpx
import json

SERVER_HOST = 'http://oryn.local:11434'
MODEL = 'cogito:3b'

def query(prompt: str):
    result = httpx.post(
        f'{SERVER_HOST}/api/chat',
        json={
            'model': MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        },
        timeout=20
    )

    response = ''
    for chunk in result.iter_lines():
        response += json.loads(chunk)['message']['content']

    return response

def tokenize(prompt: str):
    result = httpx.post(
        f'{SERVER_HOST}/api/embeddings',
        json={
            'model': MODEL,
            'prompt': prompt
        },
        timeout=20
    )

    return result.json()['embedding']

