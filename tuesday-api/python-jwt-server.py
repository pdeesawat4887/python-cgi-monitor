import jwt
from datetime import datetime, timedelta

class JsonWebToken:

    JWT_SECRET = 'secret'
    JWT_ALGORITHM = 'HS256'
    JWT_ISS = 'http://192.168.254.31'
    JWT_AUD = 'http://192.168.254.31'
    JWT_EXP_DELTA_SECONDS = 86400

    def create_token(self, subscriber):

        JWT_IAT=JWT_NBF = datetime.utcnow()

        payload = {
            'user': subscriber,
            'iss': self.JWT_ISS,
            'aud': self.JWT_AUD,
            'iat': JWT_IAT,
            'nbf': JWT_NBF,
            'exp': JWT_IAT + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
        }

        jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
        return jwt_token

    def decrypt_token(self, token):
        try:
            return jwt.decode(token, self.JWT_SECRET, self.JWT_ALGORITHM, audience=self.JWT_AUD)
        except jwt.ExpiredSignatureError as error:
            return self.response(error)
        except jwt.InvalidSignatureError as error:
            return self.response(error)

    def response(self, msg):
        print "Status: 401 Unauthorized\r"
        print "Content-Type: text/html\n"
        print msg
        exit()

tester = JsonWebToken()
print tester.decrypt_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwOi8vMTkyLjE2OC4yNTQuMzEiLCJ1c2VyX2lpZCI6ImFkbWluIiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguMjU0LjMxIiwiZXhwIjoxNTQwNDYwNzgxLCJpYXQiOjE1NDA0NjA3MjEsIm5iZiI6MTU0MDQ2MDcyMX0.aeNeduALnvBKGQ3DdT2QHHdmnxQ7CJvs6U214YXQuiU')
