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
        
        verified = True

        try:
            for scope in scopeList:
                if not scope in decoded_token['scp']:
                    verified = False
        except:
            return False

        return verified
