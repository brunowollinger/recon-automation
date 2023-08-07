FROM kalilinux/kali-rolling:latest

WORKDIR /data

RUN apt update

RUN apt install git golang python3 python3-pip sublist3r subfinder nmap nikto assetfinder hydra nuclei -y

RUN python3 -m pip install uuid

RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

RUN go install -v github.com/tomnomnom/waybackurls@latest

RUN go install -v github.com/openrdap/rdap/cmd/rdap@master

RUN export PATH=$PATH:/root/go/bin
