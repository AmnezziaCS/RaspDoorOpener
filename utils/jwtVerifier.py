import jwt
import json

def fluxJwtVerifier(request):
    try:
        if request.cookies.get('jwt'):
            jsonFile = open("./users.json")
            userJson = json.load(jsonFile)
            if jwt.decode(request.cookies.get('jwt'), "elhuevo", algorithms=["HS256"]).get('username') in userJson:
                return True
        return False
    except:
        return False

def cookieJwtVerifier(request):
    try:
        if request.args.get('encodedJwt'):
            jsonFile = open("./users.json")
            userJson = json.load(jsonFile)
            if jwt.decode(request.args.get('encodedJwt'), "elhuevo", algorithms=["HS256"]).get('username') in userJson:
                return True
        return False
    except:
        return False