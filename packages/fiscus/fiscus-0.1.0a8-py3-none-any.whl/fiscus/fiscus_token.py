# token.py

import time
import hmac
import hashlib

def generate_token(api_key):
    """
    Generates a token for authentication or secure communication with Fiscus backend.
    
    Args:
        api_key (str): A secret key used to generate the HMAC signature.
        
    Returns:
        str: A token in the format 'timestamp:signature'.
    """
    
    # Get the current time in seconds since the epoch as a string
    timestamp = str(int(time.time()))  
    
    # Encode the timestamp to bytes using UTF-8 encoding
    message = timestamp.encode('utf-8')  
    
    # Generate an HMAC signature using the API key and the timestamp message.
    # The signature is created using the SHA-256 hashing algorithm.
    signature = hmac.new(api_key.encode('utf-8'), message, hashlib.sha256).hexdigest()
    
    # Concatenate the timestamp and the signature into a token string with a colon separator
    token = f"{timestamp}:{signature}"
    
    # Return the generated token
    return token
