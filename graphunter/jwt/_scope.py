import jwt
import logging

class JWTScopeVerifier:    
    def __init__(self):
        self.logger = logging.getLogger("JWTScopeVerifier")
    
    def verify(self, jwt_token, scopeList):
        try:
            decoded_token = jwt.decode(jwt_token, options={'verify_signature':False})
        except jwt.InvalidTokenError:
            self.logger.error('Invalid JWT token')
            return False

        for scope in scopeList:
            if scope in decoded_token['scp']:
                return True

        return False
