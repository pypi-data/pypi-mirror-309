from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class ModelMetadata(BaseModel):
    """Model metadata schema"""
    model_id: str
    base_model: str
    created_at: datetime
    updated_at: datetime
    status: str  # e.g., "training", "ready", "failed"
    description: Optional[str] = None
    config: Dict = {}

class ModelConfig(BaseModel):
    """Model configuration schema"""
    base_model: str
    training_params: Dict
    dataset_id: str
    output_dir: str
    checkpoint_freq: Optional[int] = 1000
    eval_freq: Optional[int] = 500

class ModelPaths:
    """Model storage path generator"""
    
    @staticmethod
    def base_path(model_id: str) -> str:
        return f"models/{model_id}"
    
    @staticmethod
    def weights_path(model_id: str) -> str:
        return f"models/{model_id}/weights"
    
    @staticmethod
    def config_path(model_id: str) -> str:
        return f"models/{model_id}/config.json"
    
    @staticmethod
    def metadata_path(user_id: str) -> str:
        return f"users/{user_id}/metadata/models.json"
    