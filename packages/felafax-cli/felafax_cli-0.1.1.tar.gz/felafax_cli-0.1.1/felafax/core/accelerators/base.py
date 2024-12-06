from dataclasses import dataclass
from typing import Dict, Optional, TypeVar, Type, Any, List
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path


@dataclass
class AcceleratorConfig(ABC):
    """
    Base configuration class for accelerators.
    Provides common configuration patterns and validation.
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary representation."""
        return {"name": self.name}

    @classmethod
    @abstractmethod
    def from_dict(cls: Type["T"], data: Optional[Dict[str, Any]] = None) -> "T":
        """Create config instance from dictionary data."""
        raise NotImplementedError

    def __str__(self) -> str:
        """String representation of the config."""
        return f"{self.__class__.__name__}(name='{self.name}')"


T = TypeVar("T", bound=AcceleratorConfig)


class AcceleratorStatus(str, Enum):
    """Status for compute accelerators"""

    UNKNOWN = "unknown"
    PROVISIONING = "provisioning"
    READY = "ready"
    RUNNING = "running"
    STOPPING = "stopping"
    TERMINATED = "terminated"
    FAILED = "failed"


class AcceleratorMetrics:
    """Metrics for compute accelerators"""

    cpu_usage: float
    memory_usage: float
    gpu_usage: Optional[float] = None
    gpu_memory: Optional[float] = None
    temperature: Optional[float] = None


class AcceleratorProvider(ABC):
    """Abstract base class for compute providers"""

    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the accelerator with config"""
        pass

    @abstractmethod
    async def start(self) -> Dict[str, Any]:
        """Start the accelerator"""
        pass

    @abstractmethod
    async def stop(self) -> Dict[str, Any]:
        """Stop the accelerator"""
        pass

    @abstractmethod
    async def get_status(self) -> AcceleratorStatus:
        """Get accelerator status"""
        pass

    @abstractmethod
    async def get_metrics(self) -> AcceleratorMetrics:
        """Get accelerator metrics"""
        pass

    @abstractmethod
    async def run_command(
        self,
        command: List[str],
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run command on accelerator"""
        pass

    @abstractmethod
    async def upload_file(self, local_path: Path, remote_path: Path) -> None:
        """Upload file to accelerator"""
        pass

    @abstractmethod
    async def download_file(self, remote_path: Path, local_path: Path) -> None:
        """Download file from accelerator"""
        pass
