import os
from functools import wraps
from pathlib import Path

from flask import g, jsonify, request
import jwt
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env.local')

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev-4h501vphbrckh25y.us.auth0.com')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
ISSUER = f'https://{AUTH0_DOMAIN}/'
ALGORITHMS = ['RS256']

_jwk_client = jwt.PyJWKClient(f'{ISSUER}.well-known/jwks.json')


def _get_token_auth_header() -> str:
    auth_header = request.headers.get('Authorization', '')
    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise ValueError('Missing or invalid Authorization header')

    return parts[1]


def _verify_token(token: str) -> dict:
    if not AUTH0_AUDIENCE:
        raise RuntimeError('AUTH0_AUDIENCE is not configured')

    signing_key = _jwk_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=ALGORITHMS,
        audience=AUTH0_AUDIENCE,
        issuer=ISSUER,
    )


def require_auth(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return ('', 200)

        try:
            token = _get_token_auth_header()
            g.auth = _verify_token(token)
        except RuntimeError as exc:
            return jsonify({'error': str(exc)}), 500
        except Exception as exc:
            return jsonify({'error': f'Unauthorized: {exc}'}), 401

        return handler(*args, **kwargs)

    return wrapper