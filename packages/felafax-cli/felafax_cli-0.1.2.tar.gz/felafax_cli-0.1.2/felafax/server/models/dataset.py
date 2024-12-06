from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class DatasetMetadata(BaseModel):
    """Dataset metadata schema"""
    dataset_id: str
    name: str
    created_at: datetime
    size_bytes: int
    format: str
    stats: Optional[Dict] = {}
    
class DatasetStoragePaths:
    """Dataset storage path generator"""
    
    @staticmethod
    def base_path(user_id: str) -> str:
        return f"users/{user_id}/data"
    
    @staticmethod
    def dataset_path(user_id: str, dataset_id: str) -> str:
        return f"users/{user_id}/data/{dataset_id}"
    
    @staticmethod
    def raw_path(user_id: str, dataset_id: str) -> str:
        return f"users/{user_id}/data/{dataset_id}/raw"
    
    @staticmethod
    def processed_path(user_id: str, dataset_id: str) -> str:
        return f"users/{user_id}/data/{dataset_id}/processed"
    
    @staticmethod
    def metadata_path(user_id: str) -> str:
        return f"users/{user_id}/metadata/datasets.json"
    