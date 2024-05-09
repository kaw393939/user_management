from datetime import datetime, timedelta, timezone
import logging
import jwt
from settings.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    logging.debug(f"Starting token creation. Data: {data}")
    to_encode = data.copy()
    
    # Convert 'role' to uppercase before encoding the JWT, if present
    if 'role' in to_encode:
        to_encode['role'] = to_encode['role'].upper()
        logging.debug(f"'role' modified to uppercase: {to_encode['role']}")
    
    # Check for required fields in the token payload
    if 'user_id' not in to_encode:
        logging.error("Missing 'user_id' in token payload")
        raise ValueError("user_id is required in the token payload")
    
    # Set the expiration time for the token using timezone-aware datetime
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire.timestamp()})  # Store as timestamp
    logging.debug(f"Token expiration set to {expire.isoformat()}")
    
    # Encode the JWT
    try:
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        logging.info(f"JWT created with expiration at {expire.isoformat()}")
        logging.debug(f"Encoded JWT: {encoded_jwt}")
        
        # Immediate decoding test to verify correctness right after creation
        try:
            decoded = jwt.decode(encoded_jwt, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            logging.info("Immediate decode result: {}".format(decoded))
            logging.debug("Immediate decode check: {}".format(decoded))
        except jwt.ExpiredSignatureError:
            logging.error("Token already expired upon creation, check system clock.")
        except jwt.InvalidTokenError as e:
            logging.error(f"Token invalid right after creation: {e}")
        except jwt.PyJWTError as e:
            logging.error(f"Error during immediate token decode: {e}")
        
        return encoded_jwt
    except Exception as e:
        logging.error(f"Error encoding JWT: {e}")
        raise

def decode_token(token: str):
    logging.info(f"Attempting to decode token: {token}")
    try:
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        logging.info("JWT decoded successfully")
        logging.debug(f"Decoded JWT payload: {decoded}")
        
        # Comparing timestamps using UTC now
        current_timestamp = datetime.now(timezone.utc).timestamp()
        exp_timestamp = decoded.get("exp")
        
        logging.info(f"Current timestamp: {current_timestamp}")
        logging.info(f"Token expiration timestamp: {exp_timestamp}")
        
        if current_timestamp > exp_timestamp:
            logging.warning("Token has expired.")
            return None
        
        return decoded
    except jwt.ExpiredSignatureError:
        logging.warning("Attempt to access with expired token.")
        return None
    except jwt.InvalidTokenError:
        logging.error("Invalid token detected.")
        return None
    except jwt.PyJWTError as e:
        logging.error(f"JWT decoding failed: {e}")
        return None
