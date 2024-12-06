from fastapi import FastAPI
from ..config import Config
import uvicorn
from .api.auth import router as auth_router
from .api.finetune import router as finetune_router
from .api.models import router as models_router
from .api.dataset import router as dataset_router
from .api.billing import router as billing_router
from .api.models import router as models_router
import logging

app = FastAPI(
    debug=False,  # Config.DEBUG,
    title="Felafax API",
    description="API for the Felafax server",
    version="0.1.0"
)

app.include_router(auth_router)
app.include_router(finetune_router)
app.include_router(models_router)
app.include_router(dataset_router)
app.include_router(billing_router)

# setup logger
logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)

if __name__ == "__main__":
    uvicorn.run(
       "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )
