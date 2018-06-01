# You need a certificate+key file to serve HTTPS. Use for instance let's encrypt. ! MUST CHANGE !
CERT = {
    'crt': '/path/to/cert.pem',
    'key': '/path/to/privkey.pem'
}
# Settings for OIDC
oidc = {
    'ISSUER_ID': 'https://preprod.signicat.com/oidc/',      # Base URI
    'CLIENT_ID': 'demo-preprod',                            # Service name
    'SCOPE': 'openid+profile+signicat.national_id',         # Scope
    'REDIRECT_URI': 'https://example.com/redirect',       # Redirect URI ! MUST CHANGE !
    'STATE': 'ZTATE',                                       # "Placeholder" state
    'ACR_VALUES': 'urn:signicat:oidc:portal:auth-portal',   # ACR values
    'CRED64': 'ZGVtby1wcmVwcm9kOm1xWi1fNzUtZjJ3TnNpUVRPTmI3T240YUFaN3pjMjE4bXJSVmsxb3VmYTg='
    # CRED64 is base64 encoded credentials for demo-preprod service.
    # Decoded value: 'demo-preprod:mqZ-_75-f2wNsiQTONb7On4aAZ7zc218mrRVk1oufa8' (client_id:client_secret)
}
# Full URI for OIDC auth request
URI_OIDC = \
    oidc['ISSUER_ID'] + 'authorize?response_type=code&scope=' \
    + oidc['SCOPE'] + '&client_id=' + oidc['CLIENT_ID'] + '&redirect_uri=' \
    + oidc['REDIRECT_URI'] + '&state=' + oidc['STATE'] + '&acr_values=' + oidc['ACR_VALUES']
