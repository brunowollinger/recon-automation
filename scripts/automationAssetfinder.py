import sys
import socket
import requests
import uuid
import subprocess
import json
import time

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
domain = sys.argv[2]
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
url = f'https://localhost:9200/{target}-subdomain/_doc?refresh'
hora = time.strftime("%Y-%m-%dT%H:%M:%S%Z")
scanner = 'assetfinder'
auth = ('admin', 'admin')
x = str(uuid.uuid1()).split('-')[0]
container_name = f'{target}{x}-assetfinder'
output = f'assetfinder-{x}.txt'

def get_ipblock(ip):
    try:
        consulta_ipblock = requests.get(f'https://rdap.db.ripe.net/ip/{ip}')
        json_rdap = consulta_ipblock.json()
        return json_rdap['handle']
    except:
        return ''

def get_domain(domain):
    nameservers = ''
    try:
        consulta_domain = requests.get(f'https://rdap.registro.br/domain/{domain}')
        json_rdap = consulta_domain.json()
        for nameserver in json_rdap['nameservers']:
            nameservers = nameservers + nameserver['ldhName'] + ','
        nameservers.rstrip(',')
        return nameservers
    except:
        return ''

def get_ip(address):
    try:
        ip = socket.gethostbyname(address)
        return ip
    except:
        return '0.0.0.0'

def execute():    
    subprocess.check_output(f'docker run --entrypoint bash --rm --name {container_name} -v /docker/data/{target}/tmp:/data kalilinux/kali-tools:2.0 -c "assetfinder -subs-only {domain} > /data/{output}" || true', shell=True)

def parse():
    with open(f'/docker/data/{target}/tmp/{output}') as file:
        for line in file:
            line = line.rstrip('\n')
            ip = get_ip(line)
            data = {
                "@timestamp": hora,
                "server.address": line,
                "server.domain": line,
                "vulnerability.scanner.vendor": scanner,
                "server.ip": ip,
                "server.ipblock": get_ipblock(ip),
                "server.nameserver": get_domain(line)
            }
            r = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
            if r.status_code == 201:
                print('\033[32m[OK] Entry added successfully\033[0m')
                continue
            print(f'\033[31m [ERROR] {r.status_code}, Entry not added\033[0m')
            print(data)

def main():
    execute()
    parse()

if __name__ == '__main__':
    main()