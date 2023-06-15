from fastapi import Depends, Response
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router


@router.delete("/users/avatar")
def delete_avatar(
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> str:
    svc.s3_service.delete_files("makym8545-bucket", jwt.user_id)
    svc.repository.add_avatar_url(jwt.user_id, "")
    return Response(status_code=202)
