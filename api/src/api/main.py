"""FastAPI application entry point."""


from fastapi import FastAPI
from scalar_fastapi import AgentScalarConfig, add_scalar_reference

from .routers import api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""


    # OpenAPI tags for better documentation organization
    openapi_tags = [
        {
            "name": "Health",
            "description": "Health check endpoints for monitoring and Kubernetes probes",
        },
        {
            "name": "Runs",
            "description": "Authentication endpoints - login, register, token refresh",
        }
   
    ]

    app = FastAPI(
        title="Experiments API",
        summary="Rest endpoints for experiments package",
        description="".strip(),
        version="0.1.0",
        openapi_tags=openapi_tags,
        contact={
            "name": "Bredda",
            "email": "mangin.laurent@gmail.com",
        },
        docs_url=None,
        redoc_url=None,
        license_info={
            "name": "MIT",
            "identifier": "MIT",
        }
    )

    # CORS middleware
    from starlette.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods= ["*"],
        allow_headers= ["*"],
        max_age=3600,  # Cache preflight response for 1 hour (3600 seconds)
    )

    add_scalar_reference(app, agent=AgentScalarConfig(disabled=True),)

    # Include API router
    app.include_router(api_router)


    return app


app = create_app()