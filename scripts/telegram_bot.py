import requests
import json

def sendMessage():
    with open('/docker/scripts/telegram-credentials.json', 'r') as file:
        credentials = json.load(file)
    apiurl = f'https://api.telegram.org/bot{credentials["token"]}/sendMessage'
    response = requests.post(apiurl, json={'chat_id': f'{credentials["chat_id"]}', 'text': 'Hello Bot, again!'})
    if response.status_code == 200:
        print("\033[32m[v] Mensagem enviada.\n\033[0m")

if __name__ == '__main__':
    sendMessage()
