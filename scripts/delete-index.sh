#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo -e "\033[31mArgument missing: Index Name\033[0m"
    exit 1
fi

curl -XDELETE https://localhost:9200/$1 --user 'admin:admin' --insecure
