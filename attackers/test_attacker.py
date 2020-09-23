import random
import re
import requests
from time import sleep

# TODO: Add random User Agent

'''
Change:
- author: your name
- service
- service_port
- flag_regex
- config

Implement the logic of the exploit in the exploit() function below
'''

submit_url  = 'http://localhost:8080/submit'
author      = "Luca"
service     = "Service Name"
port        = 12345

flag_regex  = ''
tick        = 60 # in seconds

config = {
    'debug': True,
    'check_regex': False
}

participants = 28 # the total number of teams
targets = []

def generate_targets():
    ip_blacklist = [20] # place here our IP (and others if you need to skip them)

    for i in range(1, participants + 1):
        target = {
            'team'      : str(i),
            'ip_address': f'10.10.{i}.1'
        }
        targets.append(target)

def submit_flags(target, flags):
    data = {
        "service": service,
        "team": target['team'],
        "flags": flags,
        "name": author
    }
    print(data)
    r = requests.post(
        submit_url,
        data
    )
    return r.text

valid, expired, duplicated = 0, 0, 0

def exploit(target):
    global valid, expired, duplicated
    '''
    Implement here the logic of your exploit,
    collect flags in a list and return it
    '''
    flags = []

    for i in range(5):
        rand = random.randrange(0, 100)
        if rand < 60:
            flags.append('flg{valid}')
            valid += 1
        elif 60 <= rand and rand < 80:
            flags.append('flg{expired}') 
            expired += 1
        else:
            flags.append('flg{duplicated}')
            duplicated += 1
    
    print(valid, expired, duplicated)

    return flags

if __name__ == "__main__":
    generate_targets()

    while True:
        for target in targets:
            flags = exploit(target)
            res = submit_flags(target, flags)

        sleep(tick)