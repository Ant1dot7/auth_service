from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.users.schemas import (
    CreateUserOutSchema,
    UserInSchema,
    UserOutSchema,
    UserTokenOutSchema,
    UserUpdateSchema,
)
from common.exceptions import BaseAppException
from domain.exceptions.base import BaseDomainException
from infra.exceptions.base import InfraException
from infra.exceptions.exceptions_token import BaseTokenException
from infra.exceptions.users import UserHasNoAccessException
from infra.filters.users import GetUserByTokenFilter
from logic.commands.users import (
    CreateTokenCommand,
    CreateUserCommand,
    UpdateUserAvatarCommand,
    UpdateUserDataCommand,
    UpdateUserRoleCommand,
    VerifyUserCommand,
)
from logic.container import init_container
from logic.mediator import Mediator
from logic.queries.users import GetUserByTokenQuery
from punq import Container
from starlette import status


router = APIRouter(prefix="/users", default_response_class=ORJSONResponse)

oauth2schema = OAuth2PasswordBearer(tokenUrl="users/token", scheme_name="JWT")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user_schema: UserInSchema,
        container: Container = Depends(init_container),
) -> CreateUserOutSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        user_id, *_ = await mediator.handle_command(
            CreateUserCommand(**user_schema.model_dump()),
        )
    except BaseAppException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return CreateUserOutSchema(id=user_id)


@router.post("/token", status_code=status.HTTP_200_OK)
async def token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        container: Container = Depends(init_container),
) -> UserTokenOutSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        (access_token, refresh_token), *_ = await mediator.handle_command(
            CreateTokenCommand(username=form_data.username, password=form_data.password),
        )
    except (BaseDomainException, InfraException):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid login or password")
    return UserTokenOutSchema(access_token=access_token, refresh_token=refresh_token)


@router.get("/profile", status_code=status.HTTP_200_OK)
async def profile(
        access_token: str = Depends(oauth2schema),
        container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        user = await mediator.handle_query(GetUserByTokenQuery(GetUserByTokenFilter(token=access_token)))
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserHasNoAccessException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return UserOutSchema.from_entity(user)


@router.get("/verify/{verify_token}", status_code=status.HTTP_204_NO_CONTENT)
async def verify(verify_token: str, container: Container = Depends(init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        await mediator.handle_command(VerifyUserCommand(token=verify_token))
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InfraException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/avatar", status_code=status.HTTP_204_NO_CONTENT)
async def update_avatar(
        avatar: UploadFile = File(),
        access_token: str = Depends(oauth2schema),
        container: Container = Depends(init_container),
):
    if not avatar.content_type.startswith("image"):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Send image file")
    mediator: Mediator = container.resolve(Mediator)
    try:
        await mediator.handle_command(UpdateUserAvatarCommand(token=access_token, avatar=await avatar.read()))
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.patch("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_data(
        update_data: UserUpdateSchema,
        access_token: str = Depends(oauth2schema),
        container: Container = Depends(init_container),
):
    update_dict = update_data.model_dump(exclude_none=True)
    if not update_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty data")

    mediator: Mediator = container.resolve(Mediator)
    try:
        await mediator.handle_command(UpdateUserDataCommand(token=access_token, data=update_dict))
    except BaseDomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserHasNoAccessException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.patch("/update_role", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_role(
        user_id: int = Query(..., ge=1),
        role_id: int = Query(..., ge=1),
        access_token: str = Depends(oauth2schema),
        container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        await mediator.handle_command(
            UpdateUserRoleCommand(
                token=access_token,
                user_id=user_id,
                role_id=role_id,
            ),
        )
    except BaseTokenException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except UserHasNoAccessException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except InfraException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
