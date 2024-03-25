import bcrypt
from repository.users import UsersRepository


def gen_hash(password):
    salt = bcrypt.gensalt(9)
    hashed_pass = bcrypt.hashpw(password, salt)
    return hashed_pass


async def check_password(user_name, password):

    user = await UsersRepository.find_user(user_name)
    if not user:
        return False
    password_is_correct = bcrypt.checkpw(password, user.hash)
    return password_is_correct


