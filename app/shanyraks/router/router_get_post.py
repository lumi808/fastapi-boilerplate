from fastapi import Depends, status
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
from typing import List, Dict


class GetPostResponse(AppModel):
    _id: str
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str
    media: List[str]
    coordinates: Dict
    post_id: str


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetPostResponse)
def get_post(
    id: str,
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> GetPostResponse:
    post_id = jwt.user_id
    post = svc.repository.get_post_by_id(id)
    post["post_id"] = post_id
    return post
