import datetime
import os
import jwt
import bcrypt
from repository.users import UsersRepository


async def gen_hash(data):
    try:
        password = data.encode('utf-8')
        salt = bcrypt.gensalt(12)
        hashed_pass = bcrypt.hashpw(password, salt)
        return hashed_pass
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise


async def check_password(user_name, password):
    user = await UsersRepository.find_user(user_name)
    if user is None:
        return False

    hashed_password = user.hashed_pass
    provided_password = password.encode('utf-8')

    password_is_correct = bcrypt.checkpw(provided_password, hashed_password)
    return password_is_correct


async def gen_token():
    try:
        key = os.getenv('SECRET_KEY')
        if not key:
            raise ValueError("SECRET_KEY is not set")

        life_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=8)
        token = jwt.encode({'exp': life_time}, key, algorithm="HS256")
        return token
    except jwt.PyJWTError as e:
        # Обработка ошибок, связанных с JWT
        print(f"JWT Error: {e}")
        raise  # Поднимаем исключение дальше для обработки в вызывающем коде
    except Exception as e:
        # Обработка других неожиданных ошибок
        print(f"Unexpected Error: {e}")
        raise


async def check_token(data):
    try:
        key = os.getenv('SECRET_KEY')
        jwt.decode(data, key, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        print("Error N15 - Signature has expired")
        return False
