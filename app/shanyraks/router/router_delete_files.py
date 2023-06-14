from fastapi import Depends, status, Response
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router


@router.delete("/{id}/media", status_code=status.HTTP_202_ACCEPTED)
def delete_post(
    id: str,
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> str:
    svc.s3_service.delete_files("makym8545-bucket", id)
    svc.repository.update_post_media(id, [])
    return Response(status_code=202)
