from fastapi import Depends, status
from ..service import Service, get_service
from . import router


@router.get("/{id}/comments", status_code=status.HTTP_200_OK)
def get_comments(
    id: str,
    svc: Service = Depends(get_service),
):
    comments = svc.repository.get_comments(id)
    return comments
