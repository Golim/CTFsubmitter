""" instructions for use:
you will have to set the service name, and author name in _service and _author
the exploit must be called/written into the _exploit function, see the function
doc for more info.
"""

import threading
import queue
from ictf import iCTF
import requests
from string import ascii_uppercase, digits
import random
from time import sleep
from time import time as get_sec

_service = "service_name"
_author = "ocean"
_submitter_url = 'http://submitter.local/submit'

_flg_re = r"FLG\w{13}"

# This is needed for the alternative tick method
# _tick_duration = 15*60

q = queue.Queue()

ic = iCTF()


def id_generator(size=6, chars=ascii_uppercase + digits):
    """this function will give you random IDs if those are needed in your exploit
    i.e. usernames/passwords"""
    return ''.join(random.choice(chars) for _ in range(size))


class Attacker():

    @staticmethod
    def _exploit(target):
        """
        this is the place where you want to put your exploit

        target = {
                'team_name' : "Team name",
                'ip_address' : "10.7.<team_id>.2",
                'port' : <int port number>,
                'flag_id' : "Flag ID to steal"}

        returns: a list of CORRECT flags
        """

        flags = [
            "FLG1234567890123",
            "FLGABCDEFGHI0123"]

        return flags

    def exploit(self, target):
        res = None
        try:
            flags = self._exploit(target)
            if flags:
                res = self.submit_flags(flags, target)
        except:
            pass
            return res

    def submit_flags(self, flags, target):
        r = requests.post(
            _submitter_url,
            data={
                "service": _service,
                "team": target['team_name'],
                "flags": flags,
                "name": _author})
        return r.text

    def attack(self):

        while(1):
            # if ictf is not supported you can use this method
            # get the current time before and after the attack, compute the
            # time before the next tick and then sleep
            # init_time = int(get_sec())

            threads = []
            team = ic.login("***EMAIL***", "***TOKEN***")
            targets = team.get_targets(_service)

            # ugly, spawn one thread for each target!
            for t in targets['targets']:
                # attack phase
                th = threading.Thread(None, self.exploit, args=(t,))
                threads.append(th)
                th.start()

            # maybe we should wait for threads to close

            while threading.active_count() > 1:
                sleep(0.5)

            t_info = team.get_tick_info()
            print("waiting next tick %d seconds" %
                  t_info['approximate_seconds_left'])
            # sleep until the next round
            sleep(t_info['approximate_seconds_left'])
            while(team.get_tick_info()['tick_id'] <= t_info['tick_id']):
                sleep(1)

            # Use this for the alternative tick method
            # after_time = int(get_sec())
            # sleep_time = TICK_DURATION - (after_time - init_time)
            # print("Waiting for the next tick (%d seconds)" % sleep_time)
            # sleep(sleep_time)

if __name__ == "__main__":
    a = Attacker()
    a.attack()
