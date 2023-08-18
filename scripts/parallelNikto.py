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
list_sistemas = []

def consulta():
	data = {"size":10000}
	get_doc = requests.get(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
	parse_scan = json.loads(get_doc.text)
	for x in parse_scan['hits']['hits']:
		if(str(x['_source']['url.original']) not in list_sistemas):
			list_sistemas.append(x['_source']['url.original'])

def parallel():
    if os.path.isfile(f'/docker/data/{target}/tmp/nikto_parallel.log'):
        os.system(f'rm -f /docker/data/{target}/tmp/nikto_parallel.log')
    os.system(f'touch /docker/data/{target}/tmp/nikto_parallel.log')
    with open (f'/docker/data/{target}/tmp/nikto_parallel.log','a') as file:
        for sis in list_sistemas:
            file.write(f'python3 /docker/scripts/automationNikto.py {target} {sis}\n')
    print("\033[34m[+] PROCESSANDO NIKTO\033[0m")
    os.system(f'cat /docker/data/{target}/tmp/nikto_parallel.log | parallel -u')

def main():
   consulta()
   parallel()

if __name__ == '__main__':
    main()
