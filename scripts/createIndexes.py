import requests
import sys
import json
import authSetup

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = 'https://localhost:9200/'
mappings = {
f'{target}-subdomain': {
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.domain": {"type": "keyword"},
            "server.nameserver": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.ipblock": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
},
f'{target}-portscanner': {
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "network.protocol": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "server.ipblock": {"type": "keyword"},
            "service.name": {"type": "keyword"},
            "service.state": {"type": "keyword"},
            "application.version.number": {"type": "keyword"},
            "network.transport": {"type": "keyword"},
            "network.type": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
},
f'{target}-webenum': {
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.domain": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "network.protocol": {"type": "keyword"},
            "url.path": {"type": "keyword"},
            "url.original": {"type": "keyword"},
            "url.full": {"type": "keyword"},
            "http.response.status_code": {"type": "long"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
},
f'{target}-webvuln': {
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.domain": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "network.protocol": {"type": "keyword"},
            "service.name": {"type": "keyword"},
            "http.response.status_code": {"type": "long"},
            "url.path": {"type": "keyword"},
            "url.original": {"type": "keyword"},
            "url.full": {"type": "keyword"},
            "vulnerability.name": {"type": "keyword"},
            "vulnerability.description": {"type": "keyword"},
            "vulnerability.severity": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
},
f'{target}-infravuln': {
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "network.protocol": {"type": "keyword"},
            "service.name": {"type": "keyword"},
            "vulnerability.name": {"type": "keyword"},
            "vulnerability.description": {"type": "keyword"},
            "vulnerability.severity": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
}}

indexes = [index for index in mappings.keys()]

def delete():
    for index in indexes:
        response = requests.delete(url=f'{url}{index}', headers=headers, auth=auth, verify=False).json()
        if 'acknowledged' in response.keys() and response['acknowledged'] == True:
            print(f'\033[31m[x] Excluindo Index {index}\033[0m')

def create():
    for index in indexes:
        print(f'\033[34m[+] Criando Index {index}\033[0m')
        response = requests.put(url=f'{url}{index}', headers=headers, auth=auth, data=json.dumps(mappings[f'{index}']), verify=False).json()
        if 'acknowledged' in response.keys() and response['acknowledged'] == True:
            print(f'\033[32m[+] Index {index} Criado\033[0m')

def main():
    delete()
    create()

if __name__ == '__main__':
    main()
