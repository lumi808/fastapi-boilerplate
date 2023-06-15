from fastapi import Depends
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


# class GetFavouritesResponse(AppModel):
#     post_id: str
#     adress: str


@router.get("/users/favorites/shanyraks")
def get_favourites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    favourites = svc.repository.get_user_favourites_by_id(jwt_data.user_id)
    return favourites
