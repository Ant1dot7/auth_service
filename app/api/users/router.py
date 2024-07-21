from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from punq import Container
from starlette import status

from api.users.schemas import UserInSchema, UserOutSchema
from common.exceptions import BaseAppException
from domain.exceptions.base import BaseDomainException
from infra.exceptions.base import InfraException
from infra.filters.users import GetUserByIdFilter
from logic.commands.users import CreateUserCommand, CreateTokenCommand
from logic.container import init_container
from logic.mediator.main_mediator import Mediator
from logic.queries.users import GetUserQuery

router = APIRouter(prefix='/users', default_response_class=ORJSONResponse)


@router.post('/')
async def create_user(user_schema: UserInSchema, container: Container = Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        user, *_ = await mediator.handle_command(CreateUserCommand(**user_schema.model_dump()))
    except BaseAppException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserOutSchema.from_entity(user)


@router.get('/{user_id}')
async def get_user(user_id: int, container: Container = Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        user = await mediator.handle_query(GetUserQuery(filters=GetUserByIdFilter(user_id)))
    except InfraException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except BaseAppException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserOutSchema.from_entity(user)


@router.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends(), container: Container = Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        token, *_ = await mediator.handle_command(
            CreateTokenCommand(username=form_data.username, password=form_data.password)
        )
    except (BaseDomainException,InfraException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid login or password')
    except BaseAppException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return token
