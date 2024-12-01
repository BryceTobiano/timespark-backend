from rest_framework_simplejwt.tokens import AccessToken

def get_user_id_from_token(token):
    try:
        # Decode the token and get the payload
        access_token = AccessToken(token)
        # Retrieve the user ID from the payload
        user_id = access_token['user_id']
        return user_id
    except Exception as e:
        # Handle any errors, e.g., invalid token
        return None