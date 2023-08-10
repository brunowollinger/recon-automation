#!/usr/bin/env python3

import sys
import requests
import os
import json

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
url = f'https://localhost:9200/{target}-subdomain/_search'
auth=('admin', 'admin')
dic_ip = {}

def consulta_subdomain():
	data = {"size":10000}
	get_doc = requests.get(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
	parse_scan = json.loads(get_doc.text)
	for x in parse_scan['hits']['hits']:
		if(str(x['_source']['server.domain']) not in dic_ip and str(x['_source']['server.ip'] != '0.0.0.0')):
			dic_ip[(str(x['_source']['server.domain']))] = str(x['_source']['server.ip'])

def parallel():
    if os.path.isfile(f'/docker/data/{target}/tmp/httpx_parallel.log'):
        os.system(f'rm -rf /docker/data/{target}/tmp/httpx_parallel.log')
    os.system(f'touch /docker/data/{target}/tmp/httpx_parallel.log')
    with open (f'/docker/data/{target}/tmp/httpx_parallel.log','a') as file:
        for sub in dic_ip:
            file.write(f'python3 /docker/scripts/automation-httpx.py {target} {sub} {dic_ip[sub]}\n')
    print("\033[34m[+] PROCESSANDO HTTPX\n\033[0m")
    os.system(f'cat /docker/data/{target}/tmp/httpx_parallel.log | parallel -u')

def main():
   consulta_subdomain()
   parallel() 

if __name__ == '__main__':
    main()
