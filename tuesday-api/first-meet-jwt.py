from datetime import datetime, timedelta
import jwt


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_ISS = 'http://192.168.254.31'
JWT_AUD = 'http://192.168.254.31'
JWT_EXP_DELTA_SECONDS = 60

def encode_jwt(user):
    JWT_IAT=JWT_NBF = datetime.utcnow()
    playload = {
        'user_iid': user,
        'iss': JWT_ISS,
        'aud': JWT_AUD,
        'iat': JWT_IAT,
        'nbf': JWT_NBF,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(playload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token

def decode_jwt(str, user):
    zoo = jwt.decode(str, 'plain', JWT_ALGORITHM, audience=user)
    print zoo
    print type(zoo)
    print dir(zoo)



code = encode_jwt('admin')
print code
# decode_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwOi8vMTkyLjE2OC4yNTQuMzEiLCJ1c2VyX2lpZCI6ImFkbWluIiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguMjU0LjMxIiwiZXhwIjoxNTQwNTQ2MjM4LCJpYXQiOjE1NDA0NTk4MzgsIm5iZiI6MTU0MDQ1OTgzOH0.vZsPWmHUd_zcdHHQau5rzRyXdL-sw2NDymVXrSKpkUE')
# decode_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoid2FydXQua2QiLCJleHAiOjE1NDA0NTYwMjB9.zoWIgEN8z0X9IyxDUTi2iIPtpNfSzPREMtkEVEKV4kw')

# decode_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwOi8vMTkyLjE2OC4yNTQuMzEiLCJ1c2VyX2lpZCI6ImFkbWluIiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguMjU0LjMxIiwiZXhwIjoxNTQwNDYwNTQzLCJpYXQiOjE1NDA0NjA0ODMsIm5iZiI6MTU0MDQ2MDQ4M30.3_orBKIxZYfRq-BwlRQF__8SrFxbrAbK_OFMMgoMA0k', 'http://192.168.254.31')
# decode_jwt(code, JWT_AUD)
# decode_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9')

def python_sha256():
    import hashlib
    print hashlib.sha256("playload = {'user_id': 'warut.kd','exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)}").hexdigest()

# python_sha256()



# async def login(request):
#     post_data = await request.post()
#
#     try:
#         user = User.objects.get(email=post_data['email'])
#         user.match_password(post_data['password'])
#     except (User.DoesNotExist, User.PasswordDoesNotMatch):
#         return json_response({'message': 'Wrong credentials'}, status=400)
#
#     payload = {
#         'user_id': user.id,
#         'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
#     }
#     jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
#     return json_response({'token': jwt_token.decode('utf-8')})
#
# app = web.Application()
# app.router.add_route('POST', '/login', login)