echo '\033[34m[+] Criando index SUBDOMAIN\n\033[0m'
curl -XPUT --insecure --user 'admin:admin' https://localhost:9200/$1-subdomain -H "Content-Type: application/json" -d @- <<EOF
{
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.domain": {"type": "keyword"},
            "server.nameserver": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.ipblock": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
}
EOF

echo '\033[34m[+] Criando index PORT SCANNER\n\033[0m'
curl -XPUT --insecure --user 'admin:admin' https://localhost:9200/$1-portscanner -H "Content-Type: application/json" -d @- <<EOF
{
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "network.protocol": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "server.ipblock": {"type": "keyword"},
            "service.name": {"type": "keyword"},
            "service.state": {"type": "keyword"},
            "application.version.number": {"type": "keyword"},
            "network.transport": {"type": "keyword"},
            "network.type": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
}
EOF

echo '\033[34m[+] Criando index WEB ENUM\n\033[0m'
curl -XPUT --insecure --user 'admin:admin' https://localhost:9200/$1-webenum -H "Content-Type: application/json" -d @- <<EOF
{
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.domain": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "network.protocol": {"type": "keyword"},
            "url.path": {"type": "keyword"},
            "url.original": {"type": "keyword"},
            "url.full": {"type": "keyword"},
            "http.response.status_code": {"type": "long"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
}
EOF

echo '\033[34m[+] Criando index WEB VULN\n\033[0m'
curl -XPUT --insecure --user 'admin:admin' https://localhost:9200/$1-webvuln -H "Content-Type: application/json" -d @- <<EOF
{
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.domain": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "network.protocol": {"type": "keyword"},
            "service.name": {"type": "keyword"},
            "http.response.status_code": {"type": "long"},
            "url.path": {"type": "keyword"},
            "url.original": {"type": "keyword"},
            "url.full": {"type": "keyword"},
            "vulnerability.name": {"type": "keyword"},
            "vulnerability.description": {"type": "keyword"},
            "vulnerability.severity": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
}
EOF

echo '\033[34m[+] Criando index INFRA VULN\n\033[0m'
curl -XPUT --insecure --user 'admin:admin' https://localhost:9200/$1-infravuln -H "Content-Type: application/json" -d @- <<EOF
{
    "mappings":{
        "properties":{
            "@timestamp": {"type": "date"},
            "server.address": {"type": "keyword"},
            "server.ip": {"type": "ip"},
            "server.port": {"type": "long"},
            "network.protocol": {"type": "keyword"},
            "service.name": {"type": "keyword"},
            "vulnerability.name": {"type": "keyword"},
            "vulnerability.description": {"type": "keyword"},
            "vulnerability.severity": {"type": "keyword"},
            "vulnerability.scanner.vendor": {"type": "keyword"}
        }
    }
}
EOF
