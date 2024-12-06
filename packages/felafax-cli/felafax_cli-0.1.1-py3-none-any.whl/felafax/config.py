from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv()


class Settings(BaseSettings):
    # Server settings
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True
    
    # CLI settings
    DEV: bool = True
    PROD: bool = not DEV
    PROD_URL: str = "https://api.felafax.com"
    DEV_URL: str = f"http://{HOST}:{PORT}"
    CONFIG_DIR: str = os.path.expanduser("~/.felafax")
    CONFIG_FILE: str = os.path.join(CONFIG_DIR, "config.json")
    
    # GCS settings
    GCS_BUCKET_NAME: str = "felafax-storage-v2"
    GCS_PROJECT_ID: str = "felafax-training"

    # TPU settings
    TPU_ZONE: str = "us-central1-a"
    TPU_PROJECT: str = ""
    TPU_NAME: str = ""
    TPU_ACCELERATOR_TYPE: str = ""

    # AWS settings (for future)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


Config = Settings()
