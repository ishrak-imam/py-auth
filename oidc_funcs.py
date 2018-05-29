import requests

def getToken(code):
    """ Returns a valid token with a code from user authentication
        (see https://developer.signicat.com/documentation/authentication/protocols/openid-connect/full-flow-example/)
    """
    payload = {'client_id': 'demo-preprod', 'redirect_uri': 'https://sign.dag.ninja/consume', 'grant_type': 'authorization_code', 'code': code}
    headers = {'Authorization': 'Basic ZGVtby1wcmVwcm9kOm1xWi1fNzUtZjJ3TnNpUVRPTmI3T240YUFaN3pjMjE4bXJSVmsxb3VmYTg='}
    try:
        r = requests.post("https://preprod.signicat.com/oidc/token", data=payload, headers=headers)
        resp = r.json()
    except requests.exceptions.RequestException as e:
        resp = {'error_description': str(e)}
    print(resp)
    return resp

def getUserInfo(token):
    """ Returns JSON-formatted user info with a token from getToken
        (see https://developer.signicat.com/documentation/authentication/protocols/openid-connect/full-flow-example/)
    """
    auth_str = 'Bearer ' + token
    headers = {'Authorization': auth_str}
    try:
        r = requests.get("https://preprod.signicat.com/oidc/userinfo", headers=headers)
        resp = r.json()
    except requests.exceptions.RequestException as e:
        resp = {'error_description': str(e)}
    return resp
