from fastapi import Depends, status, Response
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{id}/comments/{comment_id}", status_code=status.HTTP_200_OK)
def update_comment(
    id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> str:
    svc.repository.update_comment(comment_id, input.content)
    return Response(status_code=200)
