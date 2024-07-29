from fastapi import APIRouter, Response, status

health_router = APIRouter()


@health_router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["API Check"],
    include_in_schema=False,
)
def check():
    return Response(status_code=status.HTTP_200_OK)
