from fastapi import Depends
from app.utils import AppModel
from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from . import router


class UpdateUserRequest(AppModel):
    name: str
    phone: str
    city: str


@router.patch(
    "/users/me",
)
def update_user(
    input: UpdateUserRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> str:
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    svc.repository.update_user(user["_id"], input.name, input.phone, input.city)
    return "User data has been updated succcessfully"
