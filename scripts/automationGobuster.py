import sys
import authSetup
import requests
import subprocess
import uuid
import json
from time import strftime

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
subdomain = sys.argv[2]
ip = sys.argv[3]
sistema = sys.argv[4]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = f'https://localhost:9200/{target}-webenum/_doc?refresh'
hora = strftime("%Y-%m-%dT%H:%M:%S%Z")
scanner = 'gobuster'
x = str(uuid.uuid1()).split('-')[0]
container_name = f'{target}-{x}-gobuster'
dic_web = {}

def executa(sistema):
    result = subprocess.check_output(f'docker run --entrypoint bash --rm --name {container_name} -v /usr/share/wordlists/dirb/:/scripts:ro kalilinux/kali-tools:2.0 -c "gobuster dir --no-color -qu "{sistema}" -w /scripts/common.txt" || true', shell=True)
    return(result.decode("utf-8").rstrip('\n').replace(' ','').split('\n'))

def parse():
    list_uri = executa(sistema)
    for uri in list_uri:
        dic_web['server.address'] = subdomain
        dic_web['server.domain'] = subdomain
        dic_web['server.ip'] = ip 
        dic_web['network.protocol'] = sys.argv[5]
        dic_web['url.path'] = uri.replace('\r\x1b[2K','').split('(')[0]
        dic_web['http.response.status_code'] = uri.split(':')[1].split(')')[0]
        dic_web['url.original'] = sistema
        dic_web['server.port'] = sys.argv[6]
        dic_web['url.full'] = sistema+dic_web['url.path']
        data = {
            '@timestamp': hora,
            'server.address': subdomain,
            'server.domain': subdomain,
            'server.ip': ip,
            'server.port': dic_web['server.port'],
            'network.protocol': dic_web['network.protocol'],
            'url.path': dic_web['url.path'],
            'http.response.status_code': dic_web['http.response.status_code'],
            'url.original': dic_web['url.original'],
            'url.full': dic_web['url.original']+dic_web['url.path'],
            'vulnerability.scanner.vendor': scanner
        }    
        r = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
        if r.status_code == 201:
            print('\033[32m[OK] Entry added successfully\033[0m')
            continue
        print(f'\033[31m[ERROR] {r.status_code}, Entry not added\033[0m')
        print(data)

def main():
    parse()
    
if __name__== '__main__':
    main()

