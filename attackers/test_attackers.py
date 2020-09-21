import random
import re
import requests
from time import sleep

'''
Test attacker. It submits random flags (valid, duplicated, old) with (sort of) random authors and services
'''

submit_url  = 'http://localhost:8080/submit'
authors     = ["Matteo", "Damiano", "Giuseppi"]
services    = ["Service 1", "Service 2", "Service 3", "Service 4"]
ports       = 12345

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
    r = requests.post(
        submit_url,
        data = {
            "service": services[random.randrange(0, len(services))],
            "team": target['team'],
            "flags": flags,
            "name": authors[random.randrange(0, len(authors))]
        }
    )
    return r.text

def exploit(target):
    '''
    Implement here the logic of your exploit,
    collect flags in a list and return it
    '''
    flags = []

    rand = random.randrange(0, 100)
    if rand < 60:
        flags.append('flg{valid}')
    elif 60 <= rand and rand < 80:
        flags.append('flg{expired}') 
    else:
        flags.append('flg{duplicated}')

    return flags

if __name__ == "__main__":
    generate_targets()

    while True:
        for target in targets:
            flags = exploit(target)
            res = submit_flags(target, flags)

        sleep(tick)