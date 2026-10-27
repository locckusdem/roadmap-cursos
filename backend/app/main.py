from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Roadmap Cursos API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cursos")
@app.get("/api/cursos")
def get_cursos():
    return [
        {
            "id": 1,
            "title": "Introducción a Docker y Contenedores",
            "platform": "YouTube",
            "technology": "DevOps",
            "level": "Principiante",
            "status": "PUBLISHED"
        },
        {
            "id": 2,
            "title": "FastAPI y Arquitectura Limpia",
            "platform": "Web",
            "technology": "Python",
            "level": "Intermedio",
            "status": "PUBLISHED"
        }
    ]
