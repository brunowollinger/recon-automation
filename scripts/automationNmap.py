import xml.etree.ElementTree as ET
import sys
import authSetup
import requests
import subprocess
import uuid
import json
from time import strftime

requests.packages.urllib3.disable_warnings() # Disable SSL warning regarding missing certificates

target = sys.argv[1]
ip = sys.argv[2]
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
auth = authSetup.getCredentials()
url = f'https://localhost:9200/{target}-portscanner/_doc?refresh'
url_get = f'https://localhost:9200/{target}-subdomain/_search'
hora = strftime("%Y-%m-%dT%H:%M:%S")
scanner = 'nmap'
x = str(uuid.uuid1()).split('-')[0]
container_name = target+'-'+x+'-nmap'
saida = 'nmap-'+x+'.xml'
dic_ports = {}

def executa():
    subprocess.check_output(f'docker run --entrypoint bash --rm --name {container_name} -v /docker/data/{target}/tmp:/data kalilinux/kali-tools:2.0 -c "nmap -sSV -O -Pn {ip} -oX /data/{saida}" || true', shell=True)

def consulta(ip):
	data = {"size":10000}
	get_doc = requests.get(url_get, headers=headers, auth=auth, data=json.dumps(data), verify=False)
	parse_scan = json.loads(get_doc.text)
	for x in parse_scan['hits']['hits']:
		if(str(x['_source']['server.ip']) == str(ip)):
			return((str(x['_source']['server.ipblock'])))

def parse():
    tree = ET.parse(f'/docker/data/{target}/tmp/{saida}')
    dic_ports['os'] = 'Not Found'
    root = tree.getroot()
    for i in root.iter('nmaprun'):
        for nmaprun in i:
            if(nmaprun.tag == 'host'):
                os = nmaprun.find('os')
                if os is None:
                    dic_ports['os'] = 'Not Found'
                else:
                    osmatch = os.find('osmatch')
                    dic_ports['os'] = osmatch.attrib['name']
                for host in nmaprun:
                    if(host.tag == 'address'):
                        if(':' not in host.attrib['addr']):
                            dic_ports['ip_v4'] = host.attrib['addr']
                            dic_ports['network.type'] = host.attrib['addrtype']
                    if(host.tag == 'ports'):
                        for port in host:
                            if(port.tag == 'port'):
                                dic_ports['network.transport'] = port.attrib['protocol']
                                dic_ports['server.port'] = port.attrib['portid']
                                for itens in port:
                                    if(itens.tag == 'state'):
                                        dic_ports['service.state'] = itens.attrib['state']
                                    if(itens.tag == 'service'):
                                        try:
                                            dic_ports['network.protocol'] = itens.attrib['name']
                                        except:
                                            dic_ports['network.protocol'] = ''
                                        try:
                                            dic_ports['application.version.number'] = itens.attrib['version']
                                        except:
                                            dic_ports['application.version.number'] = ''
                                        try:
                                            dic_ports['service.name'] = itens.attrib['product']
                                        except:
                                            dic_ports['service.name'] = ''
                                        dic_ports['server.ipblock'] = consulta(ip)
                                        data = {
                    				            '@timestamp':hora,
                    				            'server.address':ip,
                    				            'network.protocol':dic_ports['network.protocol'],
                    				            'server.ip':ip,
                    				            'server.port':dic_ports['server.port'],
                    				            'server.ipblock':dic_ports['server.ipblock'],
                    				            'server.name':dic_ports['service.name'],
                    				            'server.state':dic_ports['service.state'],
                    				            'network.transport':dic_ports['network.transport'],
                    				            'network.type':dic_ports['network.type'],
                    				            'application.version.number':dic_ports['application.version.number'],
                    				            'vulnerability.scanner.vendor':scanner,
                                                'os.full':dic_ports['os']
            				                    }
                                        r = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)
                                        if r.status_code == 201:
                                            print('\033[32m[OK] Entry added successfully\033[0m')
                                            continue
                                        print(f'\033[31m [ERROR] {r.status_code}, Entry not added\033[0m')
                                        print(data)
def main():
    executa()
    parse()
    
if __name__== '__main__':
    main()
