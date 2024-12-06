from typing import Dict, Any, Optional

from enum import Enum
from dataclasses import dataclass
import uuid
import asyncio
from datetime import datetime

from ...core.accelerators.base import AcceleratorProvider, AcceleratorStatus
from ...core.accelerators.tpu import TPUProvider, TPUConfig
from ...core.storage.base import StorageProvider
from ..models.accelerator import AcceleratorMetadata, AcceleratorStoragePaths
from ..handlers.base import ListMetadataHandler
from ..common import generate_vm_name

class ModelTier(Enum):
    SMALL = "small"     # 7B models
    MEDIUM = "medium"   # 13B models
    LARGE = "large"     # 70B models

@dataclass
class AcceleratorSpec:
    provider: str
    config: Dict[str, Any]

class AcceleratorHandler:
    # Configurations for llama3 models
    MODEL_CONFIGS = {
        "llama3": {
            "8b": AcceleratorSpec(
                provider="tpu",
                config={
                    "accelerator_type": "v3-8",
                    "zone": "us-central1-a",
                }
            ),
            "13b": AcceleratorSpec(
                provider="tpu",
                config={
                    "accelerator_type": "v5p-8",
                    "zone": "us-east5-a",
                }
            ),
            "70b": AcceleratorSpec(
                provider="tpu",
                config={
                    "accelerator_type": "v5p-8",
                    "zone": "us-east5-a",
                }
            ),
            "405b": AcceleratorSpec(
                provider="tpu",
                config={
                    "accelerator_type": "v5p-32",
                    "zone": "us-east5-a",
                }
            ),
        }
    }

    def __init__(self, storage_provider: StorageProvider, user_id: str):
        self.storage_provider = storage_provider
        self.user_id = user_id
        self._provider_map = {
            "tpu": TPUProvider
        }
        self._metadata_handler = ListMetadataHandler(AcceleratorMetadata, AcceleratorStoragePaths.metadata_path(self.user_id), "accelerator_id", self.storage_provider)

    def _get_model_family(self, model_name: str) -> str:
        """Extract model family from model name"""
        return model_name.split("-")[0].lower()

    def _get_model_size(self, model_name: str) -> str:
        """Extract model size from model name"""
        return model_name.split("-")[1]

    def _get_accelerator_spec(self, model_name: str) -> AcceleratorSpec:
        """Get accelerator specification based on model"""
        model_name = model_name.lower()
        model_family = self._get_model_family(model_name)
        model_size = self._get_model_size(model_name)
        
        # Check if it's a llama3 model
        if model_family not in self.MODEL_CONFIGS:
            raise ValueError(f"Unsupported model family: {model_family}")
        
        if model_size not in self.MODEL_CONFIGS[model_family]:
            raise ValueError(f"Unsupported model size. Only 8B, 13B, 70B, and 405B models are supported.")
        
        return self.MODEL_CONFIGS[model_family][model_size]

    async def create_accelerator(
        self, 
        model_name: str,
        tune_id: str,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> AcceleratorMetadata:
        """Create and start a new accelerator"""
        spec = self._get_accelerator_spec(model_name)
        
        # Merge custom config if provided
        config = {
            "project_id": "felafax-training",
            **spec.config
        }
        if custom_config:
            config.update(custom_config)

        # Generate accelerator ID and name
        accelerator_id = f"acc_{uuid.uuid4().hex[:8]}"
        config["name"] = f"{generate_vm_name()}"

        # Create provider instance
        provider_class = self._provider_map.get(spec.provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {spec.provider}")
        
        provider = provider_class()
        await provider.initialize(config)
        
        # Create metadata
        current_time = datetime.utcnow()
        metadata = AcceleratorMetadata(
            accelerator_id=accelerator_id,
            name=config["name"],
            provider=spec.provider,
            created_at=current_time,
            updated_at=current_time,
            status=AcceleratorStatus.PROVISIONING,
            config=config,
            attached_tune_id=tune_id,
            tags=[model_name]
        )

        # Save catalog entry
        await self._metadata_handler.add(metadata)

        # Start the accelerator asynchronously
        asyncio.create_task(provider.start())

        return metadata

    async def stop_accelerator(self, accelerator_id: str) -> None:
        """Stop and cleanup an accelerator"""
        # Get accelerator metadata
        metadata = await self._metadata_handler.get_by_id(accelerator_id)
        if not metadata:
            raise ValueError(f"Accelerator {accelerator_id} not found")
        
        # Initialize provider
        provider_class = self._provider_map.get(metadata.provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {metadata.provider}")
            
        provider = provider_class()
        await provider.initialize(metadata.config)

        # Stop the accelerator asynchronously
        asyncio.create_task(provider.stop())

        # Update metadata
        metadata.status = AcceleratorStatus.TERMINATED
        metadata.updated_at = datetime.utcnow()
        await self._metadata_handler.update(metadata)

