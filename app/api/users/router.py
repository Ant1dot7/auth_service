from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from punq import Container
from starlette import status

from api.users.schemas import UserInSchema, UserOutSchema, UserTokenOutSchema
from common.exceptions import BaseAppException
from domain.exceptions.base import BaseDomainException
from infra.exceptions.base import InfraException
from infra.exceptions.token import BaseTokenException
from infra.filters.users import GetUserByTokenFilter
from logic.commands.users import CreateUserCommand, CreateTokenCommand, VerifyUserCommand
from logic.container import init_container
from logic.mediator.main_mediator import Mediator
from logic.queries.users import GetUserByTokenQuery

router = APIRouter(prefix='/users', default_response_class=ORJSONResponse)

oauth2schema = OAuth2PasswordBearer(tokenUrl="users/token", scheme_name="JWT")


@router.post('/')
async def create_user(user_schema: UserInSchema, container: Container = Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        user, *_ = await mediator.handle_command(CreateUserCommand(**user_schema.model_dump()))
    except BaseAppException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserOutSchema.from_entity(user)


@router.post('/token')
async def token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        container: Container = Depends(init_container)
) -> UserTokenOutSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        (access_token, refresh_token), *_ = await mediator.handle_command(
            CreateTokenCommand(username=form_data.username, password=form_data.password)
        )
    except (BaseDomainException, InfraException):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid login or password')
    return UserTokenOutSchema(access_token=access_token, refresh_token=refresh_token)


@router.get('/profile')
async def profile(
        token: str = Depends(oauth2schema),
        container: Container = Depends(init_container)
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        user = await mediator.handle_query(GetUserByTokenQuery(GetUserByTokenFilter(token=token)))
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InfraException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return UserOutSchema.from_entity(user)


@router.get('/verify/{token}', status_code=status.HTTP_204_NO_CONTENT)
async def verify(token: str, container: Container = Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        await mediator.handle_command(VerifyUserCommand(token=token))
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.patch('/avatar')
async def update_avatar():
    ...
