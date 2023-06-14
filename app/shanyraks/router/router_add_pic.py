from fastapi import Depends, UploadFile, status
from ..service import Service, get_service
from . import router
from typing import List


@router.post("/{id}/media", status_code=status.HTTP_200_OK)
def upload_files(
    id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
):
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename, id)
        result.append(url)

    svc.repository.update_post_media(id, result)
    return result
