from fastapi import Depends, status, Response
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    content: str


@router.post("/{id}/comments", status_code=status.HTTP_201_CREATED)
def add_comment(
    id: str,
    input: CreatePostRequest,
    svc: Service = Depends(get_service),
    jwt: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    input = {
        "post_id": id,
        "content": input.content,
    }
    svc.repository.add_comment(input)
    return Response(status_code=200)
