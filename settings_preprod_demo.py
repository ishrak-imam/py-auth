CERT = {
    'crt': '/etc/letsencrypt/live/sign.dag.ninja/cert.pem',
    'key': '/etc/letsencrypt/live/sign.dag.ninja/privkey.pem'
}
# Settings for OIDC
oidc = {
    'ISSUER_ID': 'https://preprod.signicat.com/oidc/',      # Base URI
    'CLIENT_ID': 'demo-preprod',                            # Service name
    'SCOPE': 'openid+profile+signicat.national_id',         # Scope
    'REDIRECT_URI': 'https://sign.dag.ninja/consume',       # Redirect URI
    'STATE': 'ZTATE',                                       # "Placeholder" state
    'ACR_VALUES': 'urn:signicat:oidc:portal:auth-portal',   # ACR values
    'CRED64': 'ZGVtby1wcmVwcm9kOm1xWi1fNzUtZjJ3TnNpUVRPTmI3T240YUFaN3pjMjE4bXJSVmsxb3VmYTg='
    # CRED64 is base64 encoded credentials for demo-preprod service.
    # Decoded value: 'demo-preprod:mqZ-_75-f2wNsiQTONb7On4aAZ7zc218mrRVk1oufa8' (client_id:client_secret)
}

# Settings for SAML
saml = {
    'ISSUER_ID': 'https://preprod.signicat.com/std/method/demo-saml2/', # Base URI
    'METHOD': 'idin,mobiilivarmenne,nbid,nbid-mobil,sbid,tupas',        # Methods for portal
    'PROFILE': 'standard',                                              # Profile
    'TARGET': 'https%3A%2F%2Fsign.dag.ninja%2Fconsume'                  # URL encoded string
}

# Full URI for OIDC auth request
URI_OIDC = \
    oidc['ISSUER_ID'] + 'authorize?response_type=code&scope=' \
    + oidc['SCOPE'] + '&client_id=' + oidc['CLIENT_ID'] + '&redirect_uri=' \
    + oidc['REDIRECT_URI'] + '&state=' + oidc['STATE'] + '&acr_values=' + oidc['ACR_VALUES']
# Full URI for SAML1.1 auth request
URI_SAML = \
    saml['ISSUER_ID'] + '?method=' + saml['METHOD'] + '&profile=' \
    + saml['PROFILE'] + '&target=' + saml['TARGET']
