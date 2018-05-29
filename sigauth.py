import json
import string
import random
import ssl
import base64

from flask import Flask, g, request, render_template
from xml.dom.minidom import parseString
# Here we use minidom to parse XML but you could use ElementTree, xmltodict or whatever you want...

from oidc_funcs import *
# oidc_funcs contains: getToken(code) & getUserInfo(token) - See oidc_funcs.py for details.

app = Flask(__name__)
URI_OIDC = 'https://preprod.signicat.com/oidc/authorize?response_type=code&scope=openid+profile+signicat.national_id&client_id=demo-preprod&redirect_uri=https://sign.dag.ninja/consume&state=ZTATE&acr_values=urn:signicat:oidc:portal:auth-portal'
URI_SAML2 = 'https://preprod.signicat.com/std/method/demo-saml2/?method=idin,mobiilivarmenne,nbid,nbid-mobil,sbid,tupas&profile=standard&target=https%3A%2F%2Fsign.dag.ninja%2Fconsume'


@app.route('/')
def hello_world():
    """Returns a simple template"""
    return render_template('intro.html', url_oidc=URI_OIDC.replace('ZTATE', ''.join(random.choice('ABCDEF0123456789') for _ in range(8))), url_saml2=URI_SAML2)

@app.route('/consume', methods=['GET', 'POST'])
def eat():
    """ Function that consumes BOTH OIDC response as well as SAML2 response.
        OIDC response is a GET request, SAML2 is a POST repsonse.
        Function checks the data, then loads a HTML (Jinja) template.
    """
    # Set some "defaults" for when it fails to find values.
    name = "UNDEFINED"
    natid = "UNDEFINED"
    sub = "UNDEFINED"
    if request.method == 'GET':
        # GET means we have a OIDC reponse.
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
    if request.method == 'POST':
        # POST means we have a SAML2 reponse.
        payload = base64.b64decode(request.form['SAMLResponse'])
        xmldom = parseString(payload)
        status = xmldom.getElementsByTagName('StatusCode')[0].getAttribute("Value")
        if 'Success' not in status:
            # Something went wrong - return error.
            errmsg = xmldom.getElementsByTagName('StatusMessage')[0].firstChild.data
            return render_template('error.html', err=errmsg)
        # Find values, set them accordingly.
        attribs = xmldom.getElementsByTagName('Attribute')
        for at in attribs:
            if 'plain-name' in at.getAttribute('AttributeName'):
                name = at.childNodes[0].firstChild.data
            if 'national-id' in at.getAttribute('AttributeName'):
                natid = at.childNodes[0].firstChild.data
            if 'subject-dn' in at.getAttribute('AttributeName'):
                sub = at.childNodes[0].firstChild.data
    # Everything is (hopefully) good! Return all the data with the template.
    return render_template('uinfo.html', name=name, bday=natid, sub=sub, method=('OIDC' if request.method == 'GET' else 'SAML2'))

if __name__ == '__main__':
    # Spool up a very simple webserver with HTTPS.
    context = ('/etc/letsencrypt/live/sign.dag.ninja/cert.pem', '/etc/letsencrypt/live/sign.dag.ninja/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
