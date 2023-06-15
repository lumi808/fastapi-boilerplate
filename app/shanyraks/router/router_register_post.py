from fastapi import Depends, status

from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str


class CreatePostResponse(AppModel):
    post_id: str


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreatePostResponse
)
def create_post(
    input: CreatePostRequest,
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    post_id = jwt.user_id
    coordinates = svc.here_service.get_coordinates(input.address)
    input = {
        "post_id": post_id,
        "type": input.type,
        "price": input.price,
        "address": input.address,
        "area": input.area,
        "rooms_count": input.rooms_count,
        "description": input.description,
        "coordinates": coordinates,
    }
    svc.repository.create_post(input)

    return CreatePostResponse(post_id=jwt.user_id)
