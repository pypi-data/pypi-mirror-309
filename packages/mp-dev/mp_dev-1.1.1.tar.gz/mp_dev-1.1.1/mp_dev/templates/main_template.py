def get_content():
    return """from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.config import settings
from app.DB import Migration, Connection

Migration.Base.metadata.create_all(bind=Connection.engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Erreur interne au serveur", status_code=500)
    try:
        request.state.db = Connection.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response

@app.get("/")
def read_root():
    return {"msg": "Serveur démarré"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,  # Port 8000 pour SSL
    )
"""