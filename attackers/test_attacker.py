from randagent import getRandomAgent
'''
To use randagent:
headers = {
    'User-Agent': getRandomAgent()['User-agent']
}
'''
import random
import re
import requests
import sys
from time import sleep

'''
Change:
- author: your name
- service
- service_port
- team_token
- config
- flag_regex

Implement the logic of the exploit in the exploit() function below
'''

# This is needed in case that CTFsubmitter stops working
fallback_submit_url = 'https://finals.cyberchallenge.it/submit'
team_token  = ''

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

def safe_say(msg):
    print('\n{0}'.format(msg), file=sys.__stderr__)

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

    r = requests.post(
        submit_url,
        data
    )

    if not r.status_code == 200:
        print(f'Received status code {r.status_code}, contact CTFsubmitter maintainer immediately!\nSubmitting flags to the fallback URL')
        for stolen_flag in flags:
            r = requests.post(
                fallback_submit_url,
                data = {
                    'team_token': team_token,
                    'flag': stolen_flag
                }
            )
            # TODO: provide some message about the submitted flag (accepted, duplicated, expired)

    return r.text

def exploit(target):
    '''
    Implement here the logic of your exploit,
    collect flags in a list and return it
    '''
    flags = []

    url = target['ip_address'] + '/some-endpoint'
    cookies = {'LPH_SESSID': 'session'}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': getRandomAgent()['User-agent'],
    }

    r = requests.post(url, cookies=cookies, headers=headers)


    return flags

if __name__ == "__main__":
    generate_targets()

    try:
        print("Running! Hit CTRL+C to exit!")
        
        while True:
            for target in targets:
                flags = exploit(target)
                res = submit_flags(target, flags)

            sleep(tick)

    except (KeyboardInterrupt, SystemExit):
        safe_say("Closing...")