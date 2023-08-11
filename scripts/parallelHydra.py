import sys
import requests
import os
import json

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
url = f'https://localhost:9200/{target}-portscanner/_search'
auth=('admin', 'admin')
list_ip = []
list_serv = []
dic_ip = {}
servicos = ['ftp','ssh','pop3','telnet','imap','mysql']

def consulta():
    data = {"size":10000}
    get_doc = requests.get(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
    parse_scan = json.loads(get_doc.text)
    return parse_scan

def parallel():
    if os.path.isfile(f'/docker/data/{target}/tmp/hydra_parallel.log'):     
        os.system(f'rm -rf /docker/data/{target}/tmp/hydra_parallel.log')
    os.system(f'touch /docker/data/{target}/tmp/hydra_parallel.log')
    parse_scan = consulta()
    for x in parse_scan['hits']['hits']:
        if(x['_source']['server.ip'] not in list_ip):
            list_ip.append(x['_source']['server.ip'])
    with open (f'/docker/data/{target}/tmp/hydra_parallel.log','a') as file:
        for i in list_ip:
            for x in parse_scan['hits']['hits']:
                if(x['_source']['server.ip'] == i):
                    if(x['_source']['server.port'] not in list_serv):
                        list_serv.append(x['_source']['server.port'])    
                        if(x['_source']['network.protocol'] in servicos):
                            file.write(f'python3 /docker/scripts/automationHydra.py {target} {i} {x["_source"]["server.port"]} {x["_source"]["network.protocol"]}\n')
    print("\033[34m[+] PROCESSANDO HYDRA\n\033[0m")
    os.system(f'cat /docker/data/{target}/tmp/hydra_parallel.log | parallel -u')

def main():
    consulta()
    parallel()
    
if __name__ == '__main__':
    main()
