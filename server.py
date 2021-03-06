import authfile
import driver
import json
import event
from jose import jwt
from six.moves.urllib.request import urlopen
from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import CORS, cross_origin

AUTH0_DOMAIN = authfile.a_dm
API_AUDIENCE = authfile.a_ap
ALGORITHMS = ["RS256"]

allowed_origin = ""
if not authfile.dev:
    allowed_origin = authfile.source
else:
    allowed_origin = "http://localhost:3000"

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"*": {"origins": allowed_origin}}, supports_credentials=True)

# establish connection to database
connection = driver.Database()


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header """

    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    # Splits out Auth Header to verify length and contents
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with Bearer"}, 401)

    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)

    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience="https://" + API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )

            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)

            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description": "incorrect claims please check the audience and issuer"}, 401)

            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description": "Unable to parse authentication token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)

        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    return decorated


# This needs retrieve all events for user
# Deletes all events or Gets all events
@app.route("/Api/Events", methods=["GET", "DELETE"])
@requires_auth
def events_handler():
    usr = get_sub()
    if request.method == 'GET':
        if usr != "":
            response = connection.get_events(usr)
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    elif request.method == 'DELETE':
        if usr != "":
            data = request.get_json()
            connection.del_events(usr)
            response = "Successfully cleared."
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    else:
        response = "Invalid Method"
        return jsonify(message=response)


# This needs retrieve all events for user
# Deletes all Events from Archive or Gets All Events
@app.route("/Api/Archive/Events", methods=["GET", "DELETE"])
@requires_auth
def arch_events_handler():
    usr = get_sub()
    if request.method == 'GET':
        if usr != "":
            response = connection.get_archive(usr)
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    elif request.method == 'DELETE':
        if usr != "":
            data = request.get_json()
            connection.clr_archive(usr)
            response = "Successfully cleared."
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    else:
        response = "Invalid Method"
        return jsonify(message=response)


# This needs authentication
# Adds an Event
@app.route("/Api/Event", methods=["PUT", "DELETE"])
@requires_auth
def event_handler():
    usr = get_sub()
    data = request.get_json()
    if request.method == 'PUT':
        if usr != "" and data['strId'] != "":
            e = event.Event(data['strId'], data['strEvent'], data['dtmDate'])
            connection.insert_event(e, usr)
            response = "Successfully synced."
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    elif request.method == 'DELETE':
        if usr != "" and data['strId'] != "":
            connection.del_one_event(usr, data['strId'])
            response = "Successfully deleted."
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    else:
        response = "Invalid Method"
        return jsonify(message=response)


# This needs authentication
# Adds an Event to archive or Deletes specific event from Archive
@app.route("/Api/Archive/Event", methods=["PUT", "DELETE"])
@requires_auth
def arch_event_handler():
    usr = get_sub()
    data = request.get_json()
    if request.method == 'PUT':
        if usr != "" and data['strId'] != "":
            e = event.Event(data['strId'], data['strEvent'], data['dtmDate'])
            connection.arch_event(e, usr)
            response = "Successfully synced."
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    elif request.method == 'DELETE':
        if usr != "" and data['strId'] != "":
            connection.del_one_arch(usr, data['strId'])
            response = "Successfully deleted."
            return jsonify(message=response)
        else:
            response = "Error: Couldn't identify user."
            return jsonify(message=response)
    else:
        response = "Invalid Method"
        return jsonify(message=response)


def requires_scope(required_scope):
    # Determines if the required scope is present in the Access Token
    # required_scope (str): The scope required to access the resource

    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def get_sub():
    # Get sub of user

    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("sub"):
        return unverified_claims["sub"]


if __name__ == '__main__':
    if authfile.dev:
        app.run(host='0.0.0.0', port=5000, debug=authfile.dev)
    else:
        app.run(host='0.0.0.0', port=443, debug=authfile.dev, ssl_context=('cert.pem', 'key.pem'))
