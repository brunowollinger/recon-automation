import requests
import json
import sys
import authSetup

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

index = sys.argv[1]
url = f'https://localhost:9200/{index}/_search'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
data = {'size': 10000, 'query': {'match_all': {}}}

def main():
    if not index:
        print('\033[31mError, missing argument: Index\033[0m')
    response = requests.get(url=url, headers=headers, auth=auth, data=json.dumps(data), verify=False).json()
    if response['hits']['total']['value'] == 0:
        print('\033[31m0 Entries Found\033[0m')
        return
    for entry in response['hits']['hits']:
        print(json.dumps(entry['_source'], indent=2))
    

if __name__ == '__main__':
    main()
