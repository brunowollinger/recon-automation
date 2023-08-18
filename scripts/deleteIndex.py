import requests
import sys
import authSetup

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = f'https://localhost:9200/{index}'

def main():
    try:
        index = sys.argv[1]
    except IndexError:
        print('Error - Argument Missing: Index Name')
    else:
        index = sys.argv[1]
        requests.delete(url=url, auth=auth, headers=headers, verify=False)

if __name__ == '__main__':
    main()
