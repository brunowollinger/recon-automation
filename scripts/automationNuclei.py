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
    

    # with open(f'/docker/data/{target}/tmp/{saida}') as jsonfile:
    #     for linejson in jsonfile:
    #         jsonline = linejson.rstrip('\n')
    #         jsondata = json.loads(jsonline)
    #         for i in jsondata:
    #             if('http' in jsondata['matched-at'] or 'https' in jsondata['matched-at']):
    #                 url = f'https://localhost:9200/{target}-webvuln/_doc?refresh'
    #                 dic_web['vulnerability.name'] = jsondata['info']['name']
    #                 dic_web['vulnerability.severity'] = jsondata['info']['severity']
    #                 try:
    #                     dic_web['vulnerability.description']= jsondata['info']['description']
    #                 except:
    #                     dic_web['vulnerability.description'] = jsondata['info']['name']
    #                 dic_web['url.original'] = jsondata['host']
    #                 try:
    #                     dic_web['vulnerability.description'] = dic_web['vulnerability.description']+' '+jsondata['matcher-name']
    #                 except:
    #                     pass
    #                 dic_web['url.full'] = jsondata['matched-at']
    #                 try:
    #                     dic_web['server.ip'] = jsondata['ip']
    #                 except:
    #                     dic_web['server.ip'] = '0.0.0.0'
    #                 dic_web['reference'] = jsondata['info']['reference']
    #                 dic_web['network.protocol'] = jsondata['host'].split(':')[0]
    #                 dic_web['server.address'] = sys.argv[3]
    #                 dic_web['server.domain'] = dic_web['server.address']
    #                 dic_web['server.port'] = sys.argv[4]
    #                 dic_web['url.path'] = sys.argv[5]
    #                 dic_web['http.response.status_code'] = '200'

    #                 data = {
    #                 '@timestamp':hora,
    #                 'server.address':dic_web['server.address'],
    #                 'server.domain':dic_web['server.domain'],
    #                 'server.ip':dic_web['server.ip'],
    #                 'server.port':dic_web['server.port'],
    #                 'network.protocol':dic_web['network.protocol'],
    #                 'service.name' : 'N/A',
    #                 'url.path':dic_web['url.path'],
    #                 'http.response.status_code':dic_web['http.response.status_code'],
    #                 'vulnerability.description':dic_web['vulnerability.description'],
    #                 'vulnerability.name':dic_web['vulnerability.name'],
    #                 'vulnerability.severity':dic_web['vulnerability.severity'],
    #                 'url.original':dic_web['url.original'],
    #                 'url.full':dic_web['url.full'],
    #                 'vulnerability.scanner.vendor':scanner
    #                 }
    #             else:
    #                 url = f'https://localhost:9200/{target}-infravuln/_doc?refresh'
    #                 dic_infra['server.address'] = sys.argv[3]
    #                 dic_infra['vulnerability.name'] = jsondata['info']['name']
    #                 dic_infra['vulnerability.severity'] = jsondata['info']['severity']
    #                 try:
    #                    dic_infra['vulnerability.description'] = jsondata['info']['description']
    #                 except:
    #                     dic_infra['vulnerability.description']= jsondata['info']['name']
    #                 try:
    #                     dic_infra['vulnerability.description'] = dic_infra['vulnerability.description']+' '+jsondata['matcher-name']
    #                 except:
    #                     pass
    #                 try:
    #                     dic_infra['server.ip'] = jsondata['ip']
    #                 except:
    #                     dic_infra['server.ip'] = '0.0.0.0'
    #                 try:
    #                     dic_infra['server.port'] = jsondata['matched-at'].split(':')[1]
    #                 except:
    #                     dic_infra['server.port'] = sys.argv[4]
    #                 dic_infra['network.protocol'] = 'N/A'
    #                 if(dic_infra['server.port'] == '22'):
    #                     dic_infra['network.protocol'] = 'ssh'
    #                 if(dic_infra['server.port'] == '21'):
    #                     dic_infra['network.protocol'] = 'ftp'
    #                 if(dic_infra['server.port'] == '23'):
    #                     dic_infra['network.protocol'] = 'telnet'
    #                 if(dic_infra['server.port'] == '3389'):
    #                     dic_infra['network.protocol'] = 'rdp'
    #                 data = {
    #                 '@timestamp':hora,
    #                 'server.address':dic_infra['server.address'],
    #                 'server.ip':dic_infra['server.ip'],
    #                 'server.port':dic_infra['server.port'],
    #                 'network.protocol':dic_infra['network.protocol'],
    #                 'service.name' : 'N/A',
    #                 'vulnerability.description':dic_infra['vulnerability.description'],
    #                 'vulnerability.name':dic_infra['vulnerability.name'],
    #                 'vulnerability.severity':dic_infra['vulnerability.severity'],
    #                 'vulnerability.scanner.vendor':scanner
    #                 }
    #         r = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
    #         if r.status_code == 201:
    #             print('\033[32m[OK] Entry added successfully\033[0m')
    #             continue
    #         print(f'\033[31m [ERROR] {r.status_code}, Entry not added\033[0m')
    #         print(data)

def main():
    parse()
    
if __name__== '__main__':
    main()
