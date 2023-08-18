import requests
import json
import sys
import authSetup

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

index = sys.argv[1]
url = f'https://localhost:9200/{index}/_delete_by_query'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
data = {'size': 10000, 'query': {'match_all': {}}}

def main():
    if not index:
        print('\033[31mError, missing argument: Index\033[0m')
    response = requests.post(url=url, headers=headers, auth=auth, data=json.dumps(data), verify=False).json()
    print(f'\033[31m{response["deleted"]} Entries Deleted\033[0m')

if __name__ == '__main__':
    main()
