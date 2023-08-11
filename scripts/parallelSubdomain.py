import sys
import os

target = sys.argv[1]
domain = sys.argv[2]

def parallel():
    if os.path.isfile(f'/docker/data/{target}/tmp/subdomain_parallel.log'):
        os.system(f'rm -f /docker/data/{target}/tmp/subdomain_parallel.log')
    os.system(f'touch /docker/data/{target}/tmp/subdomain_parallel.log')
    with open (f'/docker/data/{target}/tmp/subdomain_parallel.log','w') as file:
        file.write(f'python3 /docker/scripts/automationAssetfinder.py {target} {domain}\n')
        file.write(f'python3 /docker/scripts/automationSubfinder.py {target} {domain}\n')
        # Sublist3r will not be executed because it gives no response back
        # file.write(f'python3 /docker/scripts/automationSublist3r.py {target} {domain}\n')
    print("\033[34m[+] PROCESSANDO SUBDOMAIN\n\033[0m")
    os.system(f'cat /docker/data/{target}/tmp/subdomain_parallel.log | parallel -u')

def main():
    parallel()

if __name__ == '__main__':
    main()
