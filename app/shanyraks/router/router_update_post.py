from fastapi import Depends, status, Response
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router


class UpdateUserRequest(AppModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{id}", status_code=status.HTTP_200_OK)
def update_post(
    id: str,
    input: UpdateUserRequest,
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> str:
    svc.repository.update_post(
        id,
        input.type,
        input.price,
        input.address,
        input.area,
        input.rooms_count,
        input.description,
    )
    return Response(status_code=200)
