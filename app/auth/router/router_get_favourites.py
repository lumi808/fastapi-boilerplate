from fastapi import Depends
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from app.shanyraks.service import Service as shanyraks_service
from app.shanyraks.service import get_service as shanyraks_get_service

# class GetFavouritesResponse(AppModel):
#     post_id: str
#     adress: str


@router.get("/users/favorites/shanyraks")
def get_favourites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    shan_svc: shanyraks_service = Depends(shanyraks_get_service),
):
    res = []
    favourites = list(svc.repository.get_user_favourites_by_id(jwt_data.user_id))
    for fav in favourites:
        post = shan_svc.repository.get_post_by_id(fav)
        res.append(post)
    return res
