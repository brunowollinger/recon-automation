import requests
import json
import sys

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

index = sys.argv[1]
url = f'https://localhost:9200/{index}/_search'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = ('admin', 'admin')
data = {'size': 10000, 'query': {'match_all': {}}}

def main():
    if not index:
        print('\033[31mError, missing argument: Index\033[0m')
    response = requests.get(url=url, headers=headers, auth=auth, data=json.dumps(data), verify=False).json()
    for entry in response['hits']['hits']:
        print(json.dumps(entry['_source'], indent=2))
    

if __name__ == '__main__':
    main()
