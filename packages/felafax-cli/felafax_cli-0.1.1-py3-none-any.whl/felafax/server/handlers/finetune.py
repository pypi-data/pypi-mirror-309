from ...core.storage.base import StorageProvider
from typing import Dict, List, Tuple
from ..models.finetune import FineTuneStoragePaths
from ..handlers.base import ListMetadataHandler
from ..models.finetune import FinetuneMetadata, FinetuneStatus, FineTuneRequest
from ..handlers.accelerator import AcceleratorHandler
from ..models.dataset import DatasetStoragePaths
from ..handlers.dataset import DatasetHandler
from datetime import datetime
import uuid
import yaml
from pathlib import Path
import asyncio


class FineTuneHandler:
    def __init__(self, storage_provider: StorageProvider, user_id: str):
        self._metadata_handler = ListMetadataHandler(FinetuneMetadata, FineTuneStoragePaths.metadata_path(user_id), "tune_id", storage_provider)
        self._accelerator_handler = AcceleratorHandler(storage_provider, user_id)
        self._dataset_handler = DatasetHandler(storage_provider, user_id)

        self.storage = storage_provider
        self.user_id = user_id

    async def get_tune_info(self, tune_id: str) -> Dict:
        """Get tune metadata"""
        if not await self.check_finetune_job_exists(tune_id):
            raise ValueError("Tune not found")
        path = FineTuneStoragePaths.status_path(self.user_id, tune_id)
        return FinetuneStatus(**await self.storage.read_json(path))

    async def update_tune_info(self, tune_id: str, info: Dict) -> None:
        """Update tune metadata"""
        path = FineTuneStoragePaths.status_path(self.user_id, tune_id)
        await self.storage.write_json(path, info)

    async def get_tune_config(self, tune_id: str) -> Dict:
        """Get tune configuration"""
        path = FineTuneStoragePaths.config_path(self.user_id, tune_id)
        return await self.storage.read_yaml(path)

    async def update_tune_config(self, tune_id: str, config: Dict) -> None:
        """Update tune configuration"""
        path = FineTuneStoragePaths.config_path(self.user_id, tune_id)
        await self.storage.write_yaml(path, config)

    async def validate_dataset(self, dataset_id: str) -> bool:
        return await self._dataset_handler.validate_dataset(dataset_id)
    
    async def check_finetune_job_exists(self, tune_id: str) -> bool:
        tune = await self._metadata_handler.get_by_id(tune_id)
        return tune is not None
    
    async def get_all_finetune_jobs(self) -> List[FinetuneMetadata]:
        return await self._metadata_handler.get()

    async def start_finetune(self, request: FineTuneRequest) -> Tuple[str, str, str]:
        """Start a new fine-tuning job"""
        # Generate tune ID
        tune_id = f"tune_{uuid.uuid4().hex[:12]}"

        # Create status object
        status = FinetuneStatus(
            tune_id=tune_id,
            status="initializing",
            progress=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        # Save status
        await self.update_tune_info(tune_id, status.dict())

        # Save config
        config_yaml = yaml.dump(request.config)
        config_path = Path("/tmp") / "config.yml"
        with open(config_path, "w") as f:
            f.write(config_yaml)
            
        try:
            await self.storage.upload_file(
                config_path,
                FineTuneStoragePaths.config_path(self.user_id, tune_id)
            )
        finally:
            config_path.unlink()

        # Initialize and start accelerator
        accelerator = await self._accelerator_handler.create_accelerator(
            model_name=request.model_name,
            tune_id=tune_id,
            custom_config=request.config.get("accelerator")
        )

        # Create new tune metadata
        new_tune = FinetuneMetadata(
            tune_id=tune_id,
            model_id=None,
            dataset_id=request.dataset_id,
            base_model=request.model_name,
            status="initializing",
            accelerator_id=accelerator.accelerator_id,
            created_at=status.created_at,
            updated_at=status.updated_at
        )
        
        # Add to catalog
        await self._metadata_handler.add(new_tune)
        

        return tune_id, "initializing", "Fine-tuning job created successfully"

    async def stop_finetune(self, tune_id: str) -> Tuple[str, str, str]:
        """Stop a fine-tuning job"""
        # Get tune metadata
        tune = await self._metadata_handler.get_by_id(tune_id)
        if not tune:
            raise ValueError("Tune not found")

        current_time = datetime.utcnow()
        new_status = "stopping"

        # Stop accelerator if one exists
        if tune.accelerator_id:
            asyncio.create_task(
                self._accelerator_handler.stop_accelerator(tune.accelerator_id)
            )

        # Update both status and metadata concurrently
        async def update_status():
            status = await self.get_tune_info(tune_id)
            status.status = new_status
            status.updated_at = current_time
            await self.update_tune_info(tune_id, status.dict())

        async def update_metadata():
            tune.status = new_status
            tune.updated_at = current_time
            await self._metadata_handler.update(tune)

        await asyncio.gather(update_status(), update_metadata())

        return tune_id, new_status, "Stop signal sent to fine-tuning job"
