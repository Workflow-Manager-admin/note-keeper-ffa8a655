from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth_routes import router as auth_router
from .notes_routes import router as notes_router

openapi_tags = [
    {
        "name": "auth",
        "description": "User authentication and registration."
    },
    {
        "name": "notes",
        "description": "Endpoints related to notes CRUD."
    }
]

app = FastAPI(
    title="Note App Backend",
    description="Handles user authentication and note management via REST API.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Health Check", tags=["health"])
def health_check():
    """Endpoint to check if the service is running."""
    return {"message": "Healthy"}

app.include_router(auth_router)
app.include_router(notes_router)
