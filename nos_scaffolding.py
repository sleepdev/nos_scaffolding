import hashlib
import nos
import random
import string

class AuthException( Exception ): pass

class AuthUser( nos.Object ):
    def __init__( self, email, password ):
        nos.Object.__init__(self)
        self.email = email
        self.passhash = hashlib.md5( email + password ).hexdigest()
    @staticmethod
    def signup( email, password ):
        index_key = "AuthUser: "+email
        if index_key in nos.index:
            raise AuthException()
        else:
            nos.index[index_key] = AuthUser(email,password)
            return nos.index[index_key]
    @staticmethod
    def signin( email, password ):
        index_key = "AuthUser: "+email
        if index_key in nos.index:
            user = nos.index[index_key]
            if user.passhash==hashlib.md5(email+password).hexdigest(): 
                return user
        raise AuthException()
    @staticmethod
    def reset_password( email ):
        index_key = "AuthUser: "+email
        if index_key in nos.index:
            user = nos.index[index_key]
            password = ''.join(random.choice(string.letters) for _ in range(20))
            user.passhash = hashlib.md5( email + password ).hexdigest()
            return password
        raise AuthException()
nos.models["AuthUser"] = AuthUser
