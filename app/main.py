import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from app.cache import get_cache
from app.config.logging import setup_logger
from app.exception.custom_exceptions import ValidationError
from app.llm_adapter import get_llm_adapter
from app.metrics.prometheus_metrics import get_metrics
from app.model.models import HealthResponse, RewriteRequest, RewriteResponse
from app.service.rewrite_service import RewriteService

logger = setup_logger(__name__)

app = FastAPI()

rewrite_service = RewriteService(get_llm_adapter(), get_cache())


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=exc.status_code, content={"error": {"message": exc.detail}}
    )


@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics."""
    return PlainTextResponse(get_metrics())


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for container probes."""
    return HealthResponse(status="ok")


@app.post("/v1/rewrite", response_model=RewriteResponse)
async def rewrite_text(request: RewriteRequest):
    """Rewrite text in the specified style."""
    try:
        logger.info("Processing new rewrite request")
        result = await rewrite_service.rewrite(request.text, request.style)
        return result
    except Exception as e:
        logger.error(f"Error processing rewrite request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT"))
    host = int(os.getenv("HOST"))
    uvicorn.run(app, host=host, port=port)
