import sys
import authSetup
import requests
import os
import json

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = f'https://localhost:9200/{target}-webenum/_search'
dic_sistemas = {}

def consulta():
	data = {"size":10000}
	get_doc = requests.get(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
	parse_scan = json.loads(get_doc.text)
	for x in parse_scan['hits']['hits']:
		if(str(x['_source']['url.original']) not in dic_sistemas):
			dic_sistemas[x['_source']['url.original']] = [x['_source']['server.domain'],x['_source']['server.ip']]

def parallel():
    if os.path.isfile(f'/docker/data/{target}/tmp/wayback_parallel.log'):
        os.system(f'rm -rf /docker/data/{target}/tmp/wayback_parallel.log')
    os.system(f'touch /docker/data/{target}/tmp/wayback_parallel.log')
    with open (f'/docker/data/{target}/tmp/wayback_parallel.log','a') as file:
        for sis in dic_sistemas:
            file.write(f'python3 /docker/scripts/automationWayback.py {target} {sis} {dic_sistemas[sis][0]} {dic_sistemas[sis][1]}\n')
    print("\033[34m[+] PROCESSANDO WAYBACKURLS\033[0m")
    os.system(f'cat /docker/data/{target}/tmp/wayback_parallel.log | parallel -u')

def main():
   consulta()
   parallel() 

if __name__ == '__main__':
    main()
