from bottle import (
    post, get, run, request, abort,
    template, static_file, route, error)

@post('/submit')
def get_submission():
    flag = request.forms.get('flag')

    if 'duplicated' in flag:
        print('Received a duplicated flag')
        return 'Duplicated'

    elif 'expired' in flag:
        print('Received an expired flag')
        return 'expired'

    elif 'valid' in flag:
        print('Received a valid flag')
        return 'Accepted'

    else:
        print('Received an invalid flag')
        return "expired" # Expired, because there is no such thing as invalid at the moment

@error(500)
def handle_500_error(err):
    return "500 - Internal server error"

if __name__ == "__main__":
    run(
        host='localhost',
        port=54321,
        reloader=True,
        debug=False)
