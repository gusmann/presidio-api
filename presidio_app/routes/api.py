from fastapi import APIRouter

from presidio_app.routes import analyzer

router = APIRouter()
router.include_router(analyzer.router, prefix="/analyzer", tags=["presidio-analyzer"])