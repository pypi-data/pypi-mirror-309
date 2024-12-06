from ...core.storage.base import StorageProvider
from typing import Dict, List, Optional
from ..models.model import ModelPaths
from ..handlers.base import ListMetadataHandler
from ..models.model import ModelMetadata


class ModelHandler:
    def __init__(self, storage_provider: StorageProvider, user_id: str):
        self.storage = storage_provider
        self.user_id = user_id
        self._metadata_handler = ListMetadataHandler(ModelMetadata, ModelPaths.metadata_path(user_id), "model_id", self.storage)

    async def get_model_info(self, model_id: str) -> Dict:
        """Get model metadata"""
        return await self._metadata_handler.get_by_id(model_id)

    async def update_model_info(self, model_id: str, info: Dict) -> None:
        """Update model metadata"""
        metadata = await self._metadata_handler.get_by_id(model_id)
        metadata.update(info)
        await self._metadata_handler.update(metadata)
        
    async def get_download_url(self, model_id: str) -> str:
        """Get download URL for model weights"""
        return f"/download/{self.user_id}/models/{model_id}/weights"
    
    async def delete_model(self, model_id: str) -> None:
        """Delete a model"""
        await self._metadata_handler.delete(model_id)
        model_path = ModelPaths.model_path(self.user_id, model_id)
        await self.storage.delete_directory(model_path)

