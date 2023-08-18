import sys
import authSetup
import requests
import json

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = f'https://localhost:9200/{target}-webvuln/_search'

def consulta():
	data = {"size":10000}
	get_doc = requests.get(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
	parse_scan = json.loads(get_doc.text)
	for x in parse_scan['hits']['hits']:
		print(x['_source']['vulnerability.name'],x['_source']['vulnerability.severity'],x['_source']['vulnerability.scanner.vendor'])
            
def main():
	consulta()

if __name__ == '__main__':
	main()