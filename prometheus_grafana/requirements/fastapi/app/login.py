from fastapi_login import LoginManager
from fastapi import APIRouter, Depends
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from logger import logger
from aiocache import Cache
from aiocache.serializers import PickleSerializer
import redis.asyncio as redis
from collections import namedtuple

User = namedtuple("User", ["username", "password", "id"])

cache = Cache(
    Cache.REDIS,
    endpoint="redis",
    port=6379,
    serializer=PickleSerializer(),
    namespace="main"
)

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

secret = "fastapi-secret"

manager = LoginManager(secret, token_url='/login/token')

allowed_users = [
    {"username": "a", "password": "a", "id": "24c8baa4-40db-4dd7-83b7-fd28b09b0155"},
    {"username": "b", "password": "b", "id": "306c68cb-164e-48ab-bae1-1f4340b2548c"},
    {"username": "c", "password": "c", "id": "e587397b-5a33-4604-88ce-886024321e3d"},
    {"username": "d", "password": "d", "id": "8becfc81-d436-4f01-8b5f-a2c5e0bde4df"},
    {"username": "e", "password": "e", "id": "46f518bd-e6d8-4640-bc86-434023a1425a"},
    {"username": "f", "password": "f", "id": "9881b926-3cd0-4e9a-8f19-19744fa449e6"},
    {"username": "g", "password": "g", "id": "47916915-036a-4344-ba34-f91f8704dc78"},
    {"username": "h", "password": "h", "id": "b86fe5a3-c3c5-44be-a368-0c9357898124"},
    {"username": "i", "password": "i", "id": "e08e2df2-5693-4e4d-b631-a4c482e3d915"},
    {"username": "j", "password": "j", "id": "f1b2ab99-98a1-4920-b5cd-62b603b88b62"},
    {"username": "k", "password": "k", "id": "fff5d6d4-5b29-4b8b-bdf8-879dc004e658"},
    {"username": "l", "password": "l", "id": "98cfe59f-0008-41f6-a72e-4c850002e900"},
    {"username": "m", "password": "m", "id": "3dec4d79-6d28-4980-b964-7e27f4b1fd5a"},
    {"username": "n", "password": "n", "id": "26f79560-80eb-4495-b122-f41211cd60d0"},
    {"username": "o", "password": "o", "id": "9080a5a9-e6b4-4af0-b52f-3e8e2bd69112"},
    {"username": "p", "password": "p", "id": "ea76a8e1-4297-432a-bc21-51c95d0b3de8"},
    {"username": "q", "password": "q", "id": "76ae83b2-37f5-4780-adac-1580384f530c"},
    {"username": "r", "password": "r", "id": "e0205d6e-4477-4478-8065-1ad15847bf30"},
    {"username": "s", "password": "s", "id": "e9fa4fea-b148-4cb1-855f-3133abb11b2c"},
    {"username": "t", "password": "t", "id": "8732b4a9-9845-46ed-8155-9689f64f6814"},
    {"username": "u", "password": "u", "id": "9b675be9-ef83-4fd0-86fa-08bbfb15450b"},
    {"username": "v", "password": "v", "id": "528b6d22-1cb6-447a-bef3-2d7a047f6498"},
    {"username": "w", "password": "w", "id": "5cd647a3-cc3c-4204-8198-88882b20f553"},
    {"username": "x", "password": "x", "id": "803dbcc6-bf70-4ea3-9378-105f30a50495"},
    {"username": "y", "password": "y", "id": "6d92be02-af97-44d3-8fa3-e45ce679e109"},
    {"username": "z", "password": "z", "id": "677af515-ca17-45ab-8079-6efd2e964147"},
]

@manager.user_loader()
async def load_user(username):
    logger.debug(f"searching for user {username}")
    user = await cache.get(username)
    if not user:
        raise InvalidCredentialsException
    logger.debug(f"user {user.username} found")
    return user

def get_user_id(username, password):
    for user in allowed_users:
        if user['username'] == username:
            if password == user['password']:
                return user['id']
    raise InvalidCredentialsException

@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_id = get_user_id(form_data.username, form_data.password)
    if user_id is not None:
        access_token = manager.create_access_token(
            data=dict(sub=form_data.username)
        )
        logger.debug(f"{form_data.username} registered")
        user = User(username=form_data.username, password=form_data.password, id=user_id)
        await cache.set(form_data.username, user)
        return {'access_token': access_token, 'token_type': 'bearer'}
