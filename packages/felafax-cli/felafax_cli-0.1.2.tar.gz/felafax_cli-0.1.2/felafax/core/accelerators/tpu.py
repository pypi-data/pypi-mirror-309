from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from pathlib import Path

from google.cloud import tpu_v2
import asyncio
from google.cloud import compute_v1

from .base import AcceleratorConfig, AcceleratorProvider, AcceleratorStatus, AcceleratorMetrics


@dataclass
class TPUConfig(AcceleratorConfig):
    """TPU-specific configuration"""
    name: str
    project_id: str
    zone: str
    accelerator_type: str = "v3-8"
    runtime_version: str = "tpu-vm-tf-2.16.1-pod-pjrt"
    attach_disk: bool = False
    docker_image: Optional[str] = None
    ssh_key_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary representation."""
        return {
            **super().to_dict(),
            "project_id": self.project_id,
            "zone": self.zone,
            "accelerator_type": self.accelerator_type,
            "runtime_version": self.runtime_version,
            "attach_disk": self.attach_disk,
            "docker_image": self.docker_image,
            "ssh_key_path": self.ssh_key_path
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]] = None) -> "TPUConfig":
        """Create config instance from dictionary data."""
        if not data:
            raise ValueError("Configuration data is required")
        return cls(
            name=data.get("name", ""),
            project_id=data["project_id"],
            zone=data["zone"],
            accelerator_type=data.get("accelerator_type", "v3-8"),
            runtime_version=data.get("runtime_version", "tpu-vm-tf-2.16.1-pod-pjrt"),
            attach_disk=data.get("attach_disk", False),
            docker_image=data.get("docker_image"),
            ssh_key_path=data.get("ssh_key_path")
        )


class TPUProvider(AcceleratorProvider):
    """TPU accelerator provider implementation"""

    def __init__(self):
        self.client = tpu_v2.TpuAsyncClient()
        self.config: Optional[TPUConfig] = None
        self.node_name: Optional[str] = None

    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the TPU provider with config"""
        self.config = TPUConfig.from_dict(config)
        self.node_name = f"projects/{self.config.project_id}/locations/{self.config.zone}/nodes/{self.config.name}"

    async def _get_tpu_state(self) -> Optional[str]:
        """Get the current state of a TPU node."""
        try:
            response = await self.client.get_node(name=self.node_name)
            return response.state.name
        except Exception:
            return None

    async def _create_tpu_node(self) -> Any:
        """Create a new TPU node with an optional attached disk."""
        parent = f"projects/{self.config.project_id}/locations/{self.config.zone}"
        
        if self.config.attach_disk:
            compute_client = compute_v1.DisksClient()
            disk_config = compute_v1.Disk()
            disk_config.name = f"{self.config.name}-disk"
            disk_config.size_gb = 1000
            disk_config.type_ = f"projects/{self.config.project_id}/zones/{self.config.zone}/diskTypes/pd-standard"
            
            disk_operation = compute_client.insert(
                project=self.config.project_id,
                zone=self.config.zone,
                disk_resource=disk_config
            )
            disk_operation.result()
            disk_path = f"projects/{self.config.project_id}/zones/{self.config.zone}/disks/{self.config.name}-disk"

        node = tpu_v2.Node(
            accelerator_type=self.config.accelerator_type,
            runtime_version=self.config.runtime_version,
            network_config=tpu_v2.NetworkConfig(enable_external_ips=True)
        )

        if self.config.attach_disk:
            node.data_disks = [
                tpu_v2.AttachedDisk(
                    source_disk=disk_path,
                    mode=tpu_v2.AttachedDisk.DiskMode.READ_WRITE
                )
            ]

        request = tpu_v2.CreateNodeRequest(
            parent=parent,
            node_id=self.config.name,
            node=node
        )

        operation = await self.client.create_node(request=request)
        return await operation.result()

    async def _run_docker_container(self) -> None:
        """Run a docker container on TPU VM."""
        if not self.config.docker_image:
            return

        docker_cmd = [
            "gcloud", "compute", "tpus", "tpu-vm",
            "ssh", self.config.name,
            f"--zone={self.config.zone}",
            "--command",
            f"sudo docker pull {self.config.docker_image} && sudo docker run -d {self.config.docker_image}"
        ]
        
        process = await asyncio.create_subprocess_exec(
            *docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError("Failed to run docker container")

    async def start(self) -> Dict[str, Any]:
        """Start the TPU node"""
        if not self.config or not self.node_name:
            raise RuntimeError("Provider not initialized")

        state = await self._get_tpu_state()
        if state is None:
            response = await self._create_tpu_node()
        else:
            request = tpu_v2.StartNodeRequest(name=self.node_name)
            operation = await self.client.start_node(request=request)
            response = await operation.result()

        if self.config.docker_image:
            await self._run_docker_container()

        return {"status": "started", "response": str(response)}

    async def stop(self) -> Dict[str, Any]:
        """Stop the TPU node"""
        if not self.config or not self.node_name:
            raise RuntimeError("Provider not initialized")

        # Wait for TPU to finish creating before attempting to stop
        max_retries = 30  # Maximum number of retries (5 minutes total with 10s sleep)
        for _ in range(max_retries):
            tpu_state = await self._get_tpu_state()
            if tpu_state == "CREATING":
                await asyncio.sleep(30)  # Wait 30 seconds before checking again
                continue
            
            if tpu_state in ["READY", "RUNNING"]:
                # TPU is in a state where it can be stopped
                request = tpu_v2.StopNodeRequest(name=self.node_name)
                operation = await self.client.stop_node(request=request)
                response = await operation.result()
                return {"status": "stopped", "response": str(response)}
            
            # If TPU is already stopped or in another state, return current status
            return {"status": "already_stopped", "state": tpu_state}
        
        raise RuntimeError("Timeout waiting for TPU to finish creating before stopping")

    async def get_status(self) -> AcceleratorStatus:
        """Get TPU node status"""
        if not self.config or not self.node_name:
            raise RuntimeError("Provider not initialized")

        tpu_state = await self._get_tpu_state()
        
        # Map TPU states to AcceleratorStatus
        status_mapping = {
            "CREATING": AcceleratorStatus.PROVISIONING,
            "READY": AcceleratorStatus.READY,
            "STOPPING": AcceleratorStatus.STOPPING,
            "STOPPED": AcceleratorStatus.TERMINATED,
            "DELETING": AcceleratorStatus.TERMINATED,
            "RESTARTING": AcceleratorStatus.PROVISIONING,
            "STARTING": AcceleratorStatus.PROVISIONING,
            None: AcceleratorStatus.UNKNOWN
        }
        
        return status_mapping.get(tpu_state, AcceleratorStatus.UNKNOWN)

    async def get_metrics(self) -> AcceleratorMetrics:
        """Get TPU metrics - Note: Actual TPU metrics implementation needed"""
        # This is a placeholder - actual TPU metrics collection needed
        metrics = AcceleratorMetrics()
        metrics.cpu_usage = 0.0
        metrics.memory_usage = 0.0
        return metrics

    async def run_command(
        self,
        command: List[str],
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run command on TPU VM"""
        if not self.config:
            raise RuntimeError("Provider not initialized")

        # Construct gcloud command to run on TPU VM
        gcloud_cmd = [
            "gcloud", "compute", "tpus", "tpu-vm", "ssh",
            self.config.name,
            f"--zone={self.config.zone}",
            "--command", " ".join(command)
        ]

        process = await asyncio.create_subprocess_exec(
            *gcloud_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else ""
        }

    async def upload_file(self, local_path: Path, remote_path: Path) -> None:
        """Upload file to TPU VM using gcloud scp"""
        if not self.config:
            raise RuntimeError("Provider not initialized")

        cmd = [
            "gcloud", "compute", "tpus", "tpu-vm", "scp",
            str(local_path),
            f"{self.config.name}:{str(remote_path)}",
            f"--zone={self.config.zone}"
        ]
        
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError(f"Failed to upload file to TPU VM")

    async def download_file(self, remote_path: Path, local_path: Path) -> None:
        """Download file from TPU VM using gcloud scp"""
        if not self.config:
            raise RuntimeError("Provider not initialized")

        cmd = [
            "gcloud", "compute", "tpus", "tpu-vm", "scp",
            f"{self.config.name}:{str(remote_path)}",
            str(local_path),
            f"--zone={self.config.zone}"
        ]
        
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError(f"Failed to download file from TPU VM")
