from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ...core.storage.base import StorageProvider
from ..common import get_storage_provider
from ..models.finetune import (
    FineTuneRequest, 
    FinetuneStatus, 
    FinetuneMetadata
)
from ..handlers.finetune import FineTuneHandler
from ..common import handle_error

router = APIRouter(prefix="/fine-tune", tags=["fine-tune"])


@router.post("/{user_id}/start")
async def start_fine_tune(
    user_id: str, 
    request: FineTuneRequest,
    storage_provider: StorageProvider = Depends(get_storage_provider)
):
    try:
        handler = FineTuneHandler(storage_provider, user_id)
        
        # Validate dataset exists
        if not await handler.validate_dataset(request.dataset_id):
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Start fine-tuning
        tune_id, status, message = await handler.start_finetune(request)
        
        return {
            "tune_id": tune_id,
            "status": status,
            "message": message
        }

    except Exception as e:
        handle_error(e)

@router.get("/{user_id}/{tune_id}/status", response_model=FinetuneStatus)
async def get_tune_status(
    user_id: str, 
    tune_id: str,
    storage_provider: StorageProvider = Depends(get_storage_provider)
):
    try:
        handler = FineTuneHandler(storage_provider, user_id)
        return await handler.get_tune_info(tune_id)
    except Exception as e:
        handle_error(e)

@router.post("/{user_id}/{tune_id}/stop")
async def stop_fine_tune(
    user_id: str,
    tune_id: str,
    storage_provider: StorageProvider = Depends(get_storage_provider)
):
    try:
        handler = FineTuneHandler(storage_provider, user_id)
        tune_id, status, message = await handler.stop_finetune(tune_id)
        
        return {
            "tune_id": tune_id,
            "status": status,
            "message": message
        }

    except Exception as e:
        handle_error(e)

@router.get("/{user_id}/list", response_model=List[FinetuneMetadata])
async def list_finetune_jobs(
    user_id: str,
    storage_provider: StorageProvider = Depends(get_storage_provider)
):
    handler = FineTuneHandler(storage_provider, user_id)
    return await handler.get_all_finetune_jobs()