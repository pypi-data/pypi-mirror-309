import typer
from datetime import datetime
import yaml
from ..common import get_user_id, require_auth, get_server_uri
import httpx
from pathlib import Path
from ...core.constants import SUPPORTED_MODELS

tune_app = typer.Typer(help="Tuning commands")

@tune_app.command("init-config")
def init_config():
    """Initialize a new fine-tuning configuration file"""
    
    config = {
        'hyperparameters': {
            'learning_rate': 1e-5,
            'batch_size': 32,
            'n_epochs': 4,
            'warmup_ratio': 0.0
        },
        'lora': {
            'enabled': False,
            'r': 8,
            'alpha': 8,
            'dropout': 0.0,
        }
    }
    
    # Generate filename with date prefix
    date_suffix = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f"felafax-finetune-{date_suffix}.yml"
    
    with open(filename, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    typer.echo(f"Created fine-tuning configuration file: {filename}") 

@tune_app.command("start")
@require_auth
def start_tuning(
    model: str = typer.Option(..., help=f"Base model to fine-tune (one of: {', '.join(SUPPORTED_MODELS)})"),
    config: str = typer.Option(..., help="Path to config YAML file"),
    dataset: str = typer.Option(..., help="Dataset ID to use for training")
):
    """Start a new fine-tuning job"""
    # Validate model
    if model not in SUPPORTED_MODELS:
        typer.echo(f"Error: Invalid model. Must be one of: {', '.join(SUPPORTED_MODELS)}")
        raise typer.Exit(1)
        
    # Load and validate config file
    try:
        config_path = Path(config)
        if not config_path.exists():
            typer.echo(f"Error: Config file not found: {config}")
            raise typer.Exit(1)
            
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        typer.echo(f"Error: Invalid YAML config file: {e}")
        raise typer.Exit(1)

    # Prepare request payload
    request_data = {
        "model_name": model,
        "dataset_id": dataset,
        "config": config_data
    }

    user_id = get_user_id()
    
    # Make API request
    try:
        server_uri = get_server_uri()
        response = httpx.post(
            f"{server_uri}/fine-tune/{user_id}/start",
            json=request_data
        )
        
        if response.status_code == 200:
            result = response.json()
            typer.echo(f"Started fine-tuning job: {result['tune_id']}")
            typer.echo(f"Status: {result['status']}")
            typer.echo(f"Message: {result['message']}")
        else:
            typer.echo(f"Error: {response.status_code} - {response.text}")
            raise typer.Exit(1)
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)

@tune_app.command("list")
def list_jobs():
    """List all fine-tuning jobs"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        response = httpx.get(f"{server_uri}/fine-tune/{user_id}/list")
        response.raise_for_status()
        jobs = response.json()
        
        # Print header
        typer.echo("\nFine-tuning Jobs:")
        typer.echo("-" * 80)
        typer.echo(f"{'ID':12} | {'Model Name':20} | {'Status':10} | {'Created At'}")
        typer.echo("-" * 80)
        
        # Print each job
        for job in jobs:
            created_at = job['created_at'].split('T')[0]  # Just get the date part
            typer.echo(f"{job['tune_id']:12} | {job['base_model']:20} | {job['status']:10} | {created_at}")
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)

@tune_app.command("status")
@require_auth
def get_status(
    job_id: str = typer.Option(..., help="Job ID to check status for")
):
    """Get status of a specific fine-tuning job"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        response = httpx.get(f"{server_uri}/fine-tune/{user_id}/{job_id}/status")
        response.raise_for_status()
        status = response.json()
        
        # Print status information
        typer.echo("\nFine-tuning Job Status:")
        typer.echo("-" * 40)
        typer.echo(f"Job ID: {status['tune_id']}")
        typer.echo(f"Status: {status['status']}")
        typer.echo(f"Created: {status['created_at']}")
        typer.echo(f"Last Updated: {status['updated_at']}")
        if status.get('progress') is not None:
            typer.echo(f"Progress: {status['progress']:.1%}")
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)

@tune_app.command("stop")
@require_auth
def stop_job(
    job_id: str = typer.Option(..., help="Job ID to stop")
):
    """Stop a running fine-tuning job"""
    user_id = get_user_id()
    server_uri = get_server_uri()
    
    try:
        response = httpx.post(f"{server_uri}/fine-tune/{user_id}/{job_id}/stop")
        response.raise_for_status()
        result = response.json()
        
        typer.echo(f"Stopped fine-tuning job: {result['tune_id']}")
        typer.echo(f"Status: {result['status']}")
        typer.echo(f"Message: {result['message']}")
            
    except httpx.RequestError as e:
        typer.echo(f"Error connecting to API: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(1)

# @tune_app.command("cost")
# def get_cost(
#     job_id: str = typer.Option(..., help="Job ID to get cost for")
# ):
#     """Get cost information for a specific job"""
#     # TODO: Implement cost checking logic
#     typer.echo(f"Getting cost information for job {job_id}")

# @tune_app.command("billing")
# def get_billing(
#     history: bool = typer.Option(False, help="Show billing history")
# ):
#     """Get billing information"""
#     if history:
#         # TODO: Implement historical billing logic
#         typer.echo("Showing billing history")
#     else:
#         # TODO: Implement current billing period logic
#         typer.echo("Showing current billing period") 