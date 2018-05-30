import json
import random
import ssl

from flask import Flask, g, request, render_template

from oidc_funcs import *
# oidc_funcs contains: getToken(code) & getUserInfo(token) - See oidc_funcs.py for details.
import settings_preprod_demo as cfg
"""IMPORTANT:
    You need to change the file settings_preprod_demo.py or create a copy with
    your own setting.
    The settings in settings_preprod_demo.py are exmaple settings ONLY!
    See settings_preprod_demo.py for details.
"""

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Returns a simple template"""
    cfg.oidc['STATE'] = ''.join(random.choice('ABCDEF0123456789') for _ in range(8))
    return render_template('intro.html', url_oidc=cfg.URI_OIDC.replace('ZTATE', cfg.oidc['STATE']), state=cfg.oidc['STATE'])

@app.route('/consume')
def eat():
    """ Function that consumes OIDC response.
        OIDC response is a GET request.
        Function checks the data, then loads a HTML (Jinja) template.
    """
    # Set some "defaults" for when it fails to find values.
    name = "UNDEFINED"
    natid = "UNDEFINED"
    sub = "UNDEFINED"
    if 'auth_state' in request.cookies:
        if request.cookies.get('auth_state') != request.args.get('state'):
            # State stored in cookie IS NOT same as returned from auth - return error.
            return render_template('error.html', err='Wrong state!')
    else:
        # State cookie is missing
        return render_template('error.html', err='No state!')
    if 'error' in request.args:
        # Auth process itself returned an error (instead of code) - return error.
        return render_template('error.html', err=request.args.get('error_description'))
    # 1) Use code to get token. 2) Use token to get UserInfo.
    token = getToken(request.args.get('code'))
    if 'error_description' in token:
        # Something went wrong with getting token - return error.
        return render_template('error.html', err=token['error_description'])
    uinfo = getUserInfo(token['access_token'])
    if 'error_description' in uinfo:
        # Something went wrong with getting UserInfo - return error.
        return render_template('error.html', err=uinfo['error_description'])
    # Find values, set them accordingly.
    if 'name' in uinfo:
        name = uinfo['name']
    if 'signicat.national_id' in uinfo:
        natid = uinfo['signicat.national_id']
    else:
        if 'birthdate' in uinfo:
            natid = uinfo['birthdate']
    if 'sub' in uinfo:
        sub = uinfo['sub']
    # Everything is (hopefully) good! Return all the data with the template.
    return render_template('uinfo.html', name=name, bday=natid, sub=sub, method='OIDC')

if __name__ == '__main__':
    # Spool up a very simple webserver with HTTPS.
    context = ('/etc/letsencrypt/live/sign.dag.ninja/cert.pem', '/etc/letsencrypt/live/sign.dag.ninja/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
