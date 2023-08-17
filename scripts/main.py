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
    telegramBot.sendMessage(f'Target: {target} Step: Subdomain Enumeration Status: Complete')
    os.system(f'python3 /docker/scripts/parallelHttpx.py {target}')
    os.system(f'python3 /docker/scripts/parallelWayback.py {target}')
    os.system(f'python3 /docker/scripts/parallelGobuster.py {target}')
    telegramBot.sendMessage(f'Target: {target} Step: Web Enumeration Status: Complete')
    os.system(f'python3 /docker/scripts/parallelNmap.py {target}')
    telegramBot.sendMessage(f'Target: {target} Step: Port Scanning Status: Complete')
    os.system(f'python3 /docker/scripts/parallelNikto.py {target}')
    os.system(f'python3 /docker/scripts/parallelNuclei.py {target}')
    telegramBot.sendMessage(f'Target: {target} Step: Web Vulnerability Scanning Status: Complete')
    # os.system(f'python3 /docker/scripts/parallelHydra.py {target}')
    # telegramBot.sendMessage(f'Target: {target} Step: Infrastructure Vulnerability Scanning Status: Complete')

if __name__ == '__main__':
    main()
