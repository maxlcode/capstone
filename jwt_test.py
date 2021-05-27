from jose import jwt
import json
import sys
from urllib.request import urlopen

AUTH0_DOMAIN = 'coffeeshopuda.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'
token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImduanJTelFkenk1LTNwSWFoNEFwZCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGEuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNzQ3ODMzZjlhODFhMDA2OTRlZGU4MSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjIyMTQxMTIxLCJleHAiOjE2MjIyMjc1MjEsImF6cCI6InJ4ckw4NHQ5d1RubUxQakE4aWwyeG1VY0ZpVTlWUGZlIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiY3JlYXRlOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.iehWOIpTeXKfZ0ud6m53PyLjDbBcEdMJTPkj6i34Q9eaJsHtM8MVSnU67IJKSzP9hpOtGCey40TRAqgIonwi-IszbbRheGuRwSN7X02r1IBqfS1wVvBgrj3yV7wGzddCFKzfK_s84st8lMdGxSNWQj6po-cRAs6B7tSU2cfdr1M6zsNuQbNzvDTm6Aj2Bm2JQtllPlgV5LyCAKNTxCLtiRhfw_7zEEy-uqcZ2Sowro7mxKNVlLTrMiBaBG7cH_jt-fNCYPJP_RHPhUhvnklWkZ995ht36rOlNX1PNQGgp0igXBYvy27EVJM_8rajbb9fM319Q5kJzq_pGMZdu1unuQ'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        #print(error, file=sys.stderr)
        #print(status_code, file=sys.stderr)

# GET THE PUBLIC KEY FROM AUTH0
jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
jwks = json.loads(jsonurl.read())
# GET THE DATA IN THE HEADER
unverified_header = jwt.get_unverified_header(token)
#raise Exception('Not Implemented')
# CHOOSE OUR KEY
rsa_key = {}
if 'kid' not in unverified_header:
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Authorization malformed.'
    }, 401)

for key in jwks['keys']:
    if key['kid'] == unverified_header['kid']:
        rsa_key = {
            'kty': key['kty'],
            'kid': key['kid'],
            'use': key['use'],
            'n': key['n'],
            'e': key['e']
        }

payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
print(payload, file=sys.stderr)   