from datetime import datetime
from flask import request
import pprint

def parse_args(parser, verbose=True):
    args = parser.parse_args()
    if verbose:
        environ = {}
        environ['raw_uri'] = request.__dict__.get('environ', {}).get('RAW_URI', '')
        environ['http_host'] = request.__dict__.get('environ', {}).get('HTTP_HOST', '')
        environ['http_origin'] = request.__dict__.get('environ', {}).get('HTTP_ORIGIN', '')
        environ['http_referer'] = request.__dict__.get('environ', {}).get('HTTP_REFERER', '')
        environ['http_user_agent'] = request.__dict__.get('environ', {}).get('HTTP_USER_AGENT', '')
        environ['remote_addr'] = request.__dict__.get('environ', {}).get('REMOTE_ADDR', '')
        environ['remote_port'] = request.__dict__.get('environ', {}).get('REMOTE_PORT', '')
        environ['server_name'] = request.__dict__.get('environ', {}).get('SERVER_NAME', '')
        environ['server_port'] = request.__dict__.get('environ', {}).get('SERVER_PORT', '')
        environ['request_method'] = request.__dict__.get('environ', {}).get('REQUEST_METHOD', '')

        _args = {'args': args, 'environ': environ, 'log_type': 'request', 'datetime_utcnow': datetime.utcnow().isoformat()}
        print(f'{pprint.pformat(request.__dict__)}\n[{_args["datetime_utcnow"]}]\n{pprint.pformat(_args, width=120)}\n', flush=True)

    return args


def log_payload(payload):
    _payload = {'payload': payload, 'log_type': 'response', 'datetime_utcnow': datetime.utcnow().isoformat()}
    print(f'[{_payload["datetime_utcnow"]}]\n{pprint.pformat(_payload, width=120)}\n', flush=True)
