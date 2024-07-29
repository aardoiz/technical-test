from fastapi import FastAPI

from apps.chat.http.routers import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Prueba Técnica Alfonso Ardoiz",
        description="API para la prueba técnica",
        version="1.0.0"
    )
    app.include_router(router)
    return app


app = create_app()

