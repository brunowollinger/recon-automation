import requests
import json

def main():
    with open('telegram-credentials.json', 'r') as file:
        credentials = json.load(file)
    APIurl = f'https://api.telegram.org/bot{credentials["token"]}/sendMessage'
    response = requests.post(APIurl, json={'chat_id': f'{credentials["chat_id"]}', 'text': 'Hello Bot, again!'})
    print(response.text)

if __name__ == '__main__':
    main()