import os
import json

def setCredentials():
    with open('/docker/secrets/auth.json') as file:
        auth = json.load(file)
        os.environ['OPENDISTRO_USER'] = auth['user']
        os.environ['OPENDISTRO_PASSWORD'] = auth['password']

def getCredentials():
    setCredentials()
    return (os.environ['OPENDISTRO_USER'], os.environ['OPENDISTRO_PASSWORD'])

if __name__ == '__main__':
    setCredentials()
