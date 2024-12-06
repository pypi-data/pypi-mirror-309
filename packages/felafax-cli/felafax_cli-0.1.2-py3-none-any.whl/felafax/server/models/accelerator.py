from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from ...core.accelerators.base import AcceleratorStatus


class AcceleratorMetadata(BaseModel):
    """Accelerator metadata schema"""
    accelerator_id: str
    name: str
    provider: str
    created_at: datetime
    updated_at: datetime
    status: AcceleratorStatus
    config: Dict[str, Any]
    attached_tune_id: Optional[str] = None
    tags: List[str] = []

class AcceleratorStoragePaths:
    """Accelerator storage path generator"""
    
    @staticmethod
    def base_path(user_id: str) -> str:
        return f"users/{user_id}/accelerators"
    
    @staticmethod
    def metadata_path(user_id: str) -> str:
        return f"users/{user_id}/metadata/accelerators.json"
    