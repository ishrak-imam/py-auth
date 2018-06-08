# py-auth: OIDC
### Signicat Authentication using OpenID Connect

---

A simple implementation of Signicat Authentication via the OIDC protocol.



**Dependencies**:

* Built in: json, random, ssl
* [Flask](http://flask.pocoo.org/): Used for serving a minimal SSL-enabled web server & API.
* [Requests](http://docs.python-requests.org/en/master/): HTTP for Humans.

**The project has two main functionalities**:

1. A webserver which serves intro/welcome, results and error pages to end-user.
2. An API end-point (/consume) which functions as the callback "Redirect URI" after the user has authenticated with his "Identity Provider" (BankID, NemID, Tupas, etc)

### Application Settings
You need to change the file ```settings_preprod_demo.py``` or create a copy with your own setting. The settings in ```settings_preprod_demo.py``` are example settings ONLY!

See [```settings_preprod_demo.py```](./settings_preprod_demo.py) for details. We suggest making a new file ```settings_my-service.py``` where you store your settings then refer to that in ```oidc_auth.py``` and ```oidc_funcs.py```.

### Live Implementation
A live implementation of this repository can be found at [https://sign.dag.ninja/](https://sign.dag.ninja/).

### References
For general information about the Authentication service, please refer to [Get Started With Authentication](https://developer.signicat.com/documentation/authentication/get-started-with-authentication/).

For a full-flow OIDC example, please refer to [Full-Flow Example](https://developer.signicat.com/documentation/authentication/protocols/openid-connect/full-flow-example/).
