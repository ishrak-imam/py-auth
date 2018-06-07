import requests

import settings_preprod_demo as cfg



def getToken(code):
    """ Returns a valid token with a code from user authentication
        (see https://developer.signicat.com/documentation/authentication/protocols/openid-connect/full-flow-example/)
    """
    payload = {
        'client_id': cfg.oidc['CLIENT_ID'],
        'redirect_uri': cfg.oidc['REDIRECT_URI'],
        'grant_type': 'authorization_code',
        'code': code
    }
    headers = {'Authorization': ('Basic ' + cfg.oidc['CRED64'])}
    try:
        r = requests.post((cfg.oidc['ISSUER_ID'] + 'token'), data=payload, headers=headers)
        resp = r.json()
    except requests.exceptions.RequestException as e:
        resp = {'error_description': str(e)}
    return resp

def getUserInfo(token):
    """ Returns JSON-formatted user info with a token from getToken
        (see https://developer.signicat.com/documentation/authentication/protocols/openid-connect/full-flow-example/)
    """
    auth_str = 'Bearer ' + token
    headers = {'Authorization': auth_str}
    try:
        r = requests.get((cfg.oidc['ISSUER_ID'] + 'userinfo'), headers=headers)
        resp = r.json()
    except requests.exceptions.RequestException as e:
        resp = {'error_description': str(e)}
    return resp
