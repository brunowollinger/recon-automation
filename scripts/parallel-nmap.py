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

def consulta():
	data = {"size":10000}
	get_doc = requests.get(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
	parse_scan = json.loads(get_doc.text)
	for x in parse_scan['hits']['hits']:
		if(str(x['_source']['server.ip']) not in list_ip):
			list_ip.append(str(x['_source']['server.ip']))

def parallel():
	try:
		os.system(f'rm -rf /docker/data/{target}/tmp/nmap_parallel.log')
	except:
		for ip in list_ip:
			with open (f'/docker/data/{target}/tmp/nmap_parallel.log','a') as file:
				file.write(f'python3 /docker/scripts/automation-nmap.py {target} {ip}\n')
		print("\033[34m[+] PROCESSANDO NMAP\n\033[0m")
		os.system(f'cat /docker/data/{target}/tmp/nmap_parallel.log | parallel -u')

def main():
	consulta()
	parallel()

if __name__ == '__main__':
    main()
