from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.error.types.credentials_exception import CredentialsException
from src.repository.repo_usuario import UsuarioRepo
from src.schemas.token import TokenData

SECRET_KEY = '131e9590439e5e7bc331cfa2044861a21a2e39c021610ae2bfa7c94649d4e771'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('email')
        if not email:
            raise CredentialsException(
                'Não foi possível validar as credenciais'
            )
        token_data = TokenData(**payload)
    except JWTError:
        raise CredentialsException('Não foi possível validar as credenciais')

    usuario_repository = UsuarioRepo()

    usuario = usuario_repository.get_usuario_by_email(token_data.email)

    if usuario is None:
        raise CredentialsException('Não foi possível validar as credenciais')
    return usuario
