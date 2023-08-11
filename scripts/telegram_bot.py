import requests
import json

def sendMessage(message):
    with open('/docker/scripts/telegram-credentials.json', 'r') as file:
        credentials = json.load(file)
    apiurl = f'https://api.telegram.org/bot{credentials["token"]}/sendMessage'
    requests.post(apiurl, json={'chat_id': f'{credentials["chat_id"]}', 'text': f'{message}'})

if __name__ == '__main__':
    sendMessage('Debug Message')
