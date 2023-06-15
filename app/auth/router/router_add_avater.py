from fastapi import Depends, UploadFile
from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from . import router


@router.post("/users/avatar")
def upload_avatar(
    file: UploadFile,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    url = svc.s3_service.upload_avatar(file.file, file.filename, jwt_data.user_id)
    svc.repository.add_avatar_url(jwt_data.user_id, url)
    return url
