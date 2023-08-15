import sys
import requests
import subprocess
import uuid
import json
from time import strftime

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
ip = sys.argv[2]
porta = sys.argv[3]
servico = sys.argv[4]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
url = f'https://localhost:9200/{target}-infravuln/_doc?refresh'
auth=('admin', 'admin')
hora = strftime("%Y-%m-%dT%H:%M:%S%Z")
scanner = 'hydra'
x = str(uuid.uuid1()).split('-')[0]
container_name = target+'-'+x+'-hydra'
saida = 'hydra-'+x+'.json'
dic_infra = {}
scanner = 'hydra'

def executa(ip,porta,servico):
    subprocess.check_output(f'docker run --entrypoint bash --rm --name {container_name} -v /docker/data/{target}/tmp:/data -v /docker/scripts:/scripts kalilinux/kali-tools:2.0 -c "hydra -I -L /scripts/users.txt -P /scripts/passwords.txt -e nsr -o /data/{saida} -b json -t 1 {ip} {servico} -s {porta}" || true', shell=True)

def parse():
    executa(ip,porta,servico)
    with open(f'/docker/data/{target}/tmp/{saida}') as jsonfile:
        jsondata = json.load(jsonfile)
        for i in jsondata['results']:
            dic_infra['server.address'] = i['host']
            dic_infra['server.ip'] = ip
            dic_infra['server.port'] = i['port']
            dic_infra['network.protocol'] = i['service']
            dic_infra['service.name'] = i['service']
            dic_infra['vulnerability.description'] = 'Broken username/password '+i['login']+':'+i['password']
            dic_infra['vulnerability.name'] = 'Broken username/password'
            dic_infra['vulnerability.severity'] = 'High'
            data = {
            '@timestamp':hora,
            'server.address':dic_infra['server.address'],
            'server.ip':dic_infra['server.ip'],
            'server.port':dic_infra['server.port'],
            'network.protocol':dic_infra['network.protocol'],
            'service.name' : 'N/A',
            'vulnerability.description':dic_infra['vulnerability.description'],
            'vulnerability.name':dic_infra['vulnerability.name'],
            'vulnerability.severity':dic_infra['vulnerability.severity'],
            'vulnerability.scanner.vendor':scanner
            }
            r = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
            if r.status_code == 201:
                print('\033[32m[OK] Entry added successfully\033[0m')
                continue
            print(f'\033[31m [ERROR] {r.status_code}, Entry not added\033[0m')
            print(data)

def main():
    parse()
    
if __name__== '__main__':
    main()
