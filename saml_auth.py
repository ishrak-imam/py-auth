import json
import random
import ssl
import base64

from flask import Flask, g, request, render_template
from requests.utils import quote
from xml.dom.minidom import parseString
# Here we use minidom to parse XML but you could use ElementTree, xmltodict or whatever you want...

app = Flask(__name__)

ISSUER_ID = 'https://preprod.signicat.com/std/method/demo-saml2/'
METHOD = 'idin,mobiilivarmenne,nbid,nbid-mobil,sbid,tupas'
PROFILE = 'standard'
TARGET = quote('https://sign.dag.ninja/consume', safe='')
URI_SAML2 = ISSUER_ID + '?method=' + METHOD + '&profile='  + PROFILE + '&target=' + TARGET

""" TODO:
    1) Fix implementation: This is SAML1.1 NOT SAML2! :(
    2) Verify certificates from server.
    3) ???
    4) PROFIT?!
"""

@app.route('/')
def hello_world():
    """Returns a simple template"""
    return render_template('intro.html', url_saml2=URI_SAML2)

@app.route('/consume', methods=['POST'])
def eat():
    """ Function that consumes SAML1.1/2 response.
        SAML is a POST repsonse.
        Function checks the data, then loads a HTML (Jinja) template.
    """
    # Set some "defaults" for when it fails to find values.
    name = "UNDEFINED"
    natid = "UNDEFINED"
    sub = "UNDEFINED"
    # 1) Use code to get token. 2) Use token to get UserInfo.
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
    return render_template('uinfo.html', name=name, bday=natid, sub=sub, method='SAML')

if __name__ == '__main__':
    # Spool up a very simple webserver with HTTPS.
    context = ('/etc/letsencrypt/live/sign.dag.ninja/cert.pem', '/etc/letsencrypt/live/sign.dag.ninja/privkey.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context)
