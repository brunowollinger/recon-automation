import sys
import os
import telegramBot

def main():
    target = sys.argv[1]
    domain = sys.argv[2]

    os.system(f'python3 /docker/scripts/createIndexes.py {target}')

    if os.path.isdir(f'/docker/data/{target}/tmp'):
        os.system(f'rm -rf /docker/data/{target}')
    os.system(f'mkdir -p /docker/data/{target}/tmp')

    os.system(f'python3 /docker/scripts/parallelSubdomain.py {target} {domain}')
    telegramBot.sendMessage(f'{target} Subdomain Enumeration Complete')
    os.system(f'python3 /docker/scripts/parallelHttpx.py {target}')
    os.system(f'python3 /docker/scripts/parallelWayback.py {target}')
    os.system(f'python3 /docker/scripts/parallelGobuster.py {target}')
    telegramBot.sendMessage(f'{target} Web Enumeration Complete')
    os.system(f'python3 /docker/scripts/parallelNmap.py {target}')
    telegramBot.sendMessage(f'{target} Port Scanning Complete')
    os.system(f'python3 /docker/scripts/parallelNikto.py {target}')
    # os.system(f'python3 /docker/scripts/parallelNuclei.py {target}')
    # telegramBot.sendMessage(f'{target} Web Vulnerability Scanning Complete')
    # os.system(f'python3 /docker/scripts/parallelHydra.py {target}')
    # telegramBot.sendMessage(f'{target} Infrastructure Vulnerability Scanning Complete')

if __name__ == '__main__':
    main()
