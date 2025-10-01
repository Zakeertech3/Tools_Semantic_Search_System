from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import tools, search
from app.database.qdrant import initialize_collection
from app.config.settings import settings

app = FastAPI(title="Tool Semantic Search API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tools.router)
app.include_router(search.router)


@app.on_event("startup")
async def startup_event():
    initialize_collection()


@app.get("/")
def root():
    return {"message": "Tool Semantic Search API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)