from fastapi import Depends
from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from . import router


@router.patch(
    "/users/favorites/shanyraks/{post_id}",
)
def add_favourites(
    post_id: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> str:
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    svc.repository.add_favourties(user["_id"], post_id)

    return "User data has been updated succcessfully"
