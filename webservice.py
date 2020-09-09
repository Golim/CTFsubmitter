from bottle import (
    post, get, run, request, abort,
    template, static_file, route, error)
from config import config
import re
import os

from ipaddress import ip_address

from backend.mongodb import MongoBackend
from logger import log

# define a regex for flags
flag_regex = config.get("flag_regex", "^\w{31}=$")
service_regex = "^\w{0,32}$"

backend = MongoBackend()


@route('/static/<path:path>')
def callback(path):
    return static_file(path, './static')


@get('/stats')
def stats():
    return template('templates/stats.html')


#  web interface here
@post('/submit')
def submit_flag():
    name = request.forms.get('name')
    team = request.forms.get('team')
    service = request.forms.get('service')
    flags = request.forms.getall('flags')
    ip = request.environ.get('REMOTE_ADDR')
    ip = int(ip_address(ip))

    if not flags or not team or not service or not name:
        # bad request
        abort(400)

    if not re.match(service_regex, service):
        abort(400, "wrong format for service \w{32}")

    backend.insert_flags(
            team, service, flags,
            name, ip)


@error(500)
def handle_500_error(err):
    log.exception(err.exception)
    return "500 - Internal server error"

if __name__ == "__main__":
    if 'BOTTLE_CHILD' not in os.environ:
        log.info("Submitter service started")

    backend.cold_restart()
    # try to set all the pending task to unsubmitted (retry)
    run(
        host='localhost',
        port=8080,
        reloader=True,
        debug=config.get("debug", False))
