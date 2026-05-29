from fastapi import FastAPI
from api.routes import router as api_router
from db.database import init_db
import logging
from fastapi.responses import RedirectResponse, Response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="Optiq AI Router API",
    description="Intelligent AI Router for Cost and Energy Efficient Computing",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", include_in_schema=False)
def root():
    """Redirect root to the interactive API docs."""
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Return no content for favicon requests to avoid 404 noise in logs."""
    return Response(status_code=204)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
