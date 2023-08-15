import sys
import requests
import subprocess
import uuid
import json
from time import strftime

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
sistema = sys.argv[2]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
url = f'https://localhost:9200/{target}-webvuln/_doc?refresh'
auth=('admin', 'admin')
hora = strftime("%Y-%m-%dT%H:%M:%S%Z")
scanner = 'nuclei'
x = str(uuid.uuid1()).split('-')[0]
container_name = target+'-'+x+'-nuclei'
saida = 'nuclei-'+x+'.json'
scanner = 'nuclei'

def executa(sistema):
    subprocess.check_output(f'docker run --entrypoint bash --rm --name {container_name} -v /docker/data/{target}/tmp:/data kalilinux/kali-tools:2.0 -c "nuclei -silent -u {sistema} -jle /data/{saida}" || true', shell=True)

def parse():
    executa(sistema)
    
    with open(f'/docker/data/{target}/tmp/{saida}') as file:
        for line in file:
            document = json.loads(line)
            if 'http' not in document['matched-at']:
                url = f'https://localhost:9200/{target}-infravuln/_doc?refresh'
                data = {
                    '@timestamp': hora,
                    'server.address': sys.argv[3],
                    'server.ip': document['ip'],
                    'server.port': document['matched-at'].split(':')[1],
                    'network.protocol': 'N/A',
                    'service.name' : 'N/A',
                    'vulnerability.description': document['info']['description'],
                    'vulnerability.name': document['info']['name'],
                    'vulnerability.severity': document['info']['severity'],
                    'vulnerability.scanner.vendor': scanner
                    }
                response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
                if response.status_code == 201:
                    print('\033[32m[OK] Entry added successfully\033[0m')
                    continue
                print(f'\033[31m [ERROR] {response.status_code}, Entry not added\033[0m')
                print(data)
                continue
            url = f'https://localhost:9200/{target}-webvuln/_doc?refresh'
            data = {
                    '@timestamp': hora,
                    'server.address': sys.argv[3],
                    'server.domain': sys.argv[3],
                    'server.ip': document['ip'],
                    'server.port': sys.argv[4],
                    'network.protocol': document['host'].split(':')[0],
                    'service.name': 'N/A',
                    'url.path': sys.argv[5],
                    'http.response.status_code': '200',
                    'vulnerability.description': document['info']['description'],
                    'vulnerability.name': document['info']['name'],
                    'vulnerability.severity': document['info']['severity'],
                    'url.original': document['host'],
                    'url.full': document['matched-at'],
                    'vulnerability.scanner.vendor': scanner
                    }
            response = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
            if response.status_code == 201:
                print('\033[32m[OK] Entry added successfully\033[0m')
                continue
            print(f'\033[31m [ERROR] {response.status_code}, Entry not added\033[0m')
            print(data)
    
def main():
    parse()
    
if __name__== '__main__':
    main()
