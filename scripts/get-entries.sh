#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo -e "\033[31mArgument missing: Index Name\033[0m"
    exit 1
fi

curl -XGET --insecure --user 'admin:admin' https://localhost:9200/$1/_search -H 'Content-Type: application/json' -d @- <<EOF
{
"size": 10000,
 "query": {
    "match_all": {}
    }
}
EOF