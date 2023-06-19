from typing import List, Optional
from fastapi import Depends
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class Post(AppModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    coordinates: dict


class GetPostsResponse(AppModel):
    total: int
    objects: List[Post]


@router.get("/", response_model=GetPostsResponse)
def get_posts(
    limit: int,
    offset: int,
    rooms_count: Optional[int] = None,
    type: Optional[str] = None,
    price_from: Optional[float] = None,
    price_until: Optional[float] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[float] = None,
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_posts(
        limit,
        offset,
        rooms_count,
        type,
        price_from,
        price_until,
        latitude,
        longitude,
        radius,
    )
    return result
