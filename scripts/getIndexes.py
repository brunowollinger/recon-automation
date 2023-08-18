import requests

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = 'https://localhost:9200/_cat/indices'

def getIndexes():
    response = requests.get(url=url, auth=auth, headers=headers, verify=False).json()
    return response

if __name__ == '__main__':
    indexes = getIndexes()
    for index in indexes:
        print(index['index'])
