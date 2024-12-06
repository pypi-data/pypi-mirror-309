import typer
import httpx
from ..common import load_config, save_config, get_server_uri

auth_app = typer.Typer(help="Authentication commands")

@auth_app.command("login")
def login(
    token: str = typer.Option(..., help="Authentication token"),
    force: bool = typer.Option(False, "--force", "-f", help="Force login even if already logged in")
):
    """Login to Felafax using an authentication token"""
    config = load_config()
    
    # Check if already logged in
    if not force and config.get("token"):
        typer.echo("Already logged in. Use --force to login again.")
        raise typer.Exit(1)
    
    try:
        # Call the server API to validate token and get user_id
        server_uri = get_server_uri()
        response = httpx.post(f"{server_uri}/auth/login", json={"token": token})
        
        if response.status_code != 200:
            raise Exception("Invalid token")
            
        response_data = response.json()
        user_id = response_data["user_id"]
        token = response_data["token"]
        
        if not user_id or not token:
            raise Exception("Login failed, no user_id or token returned")
        
        config.update({
            "token": token,
            "user_id": user_id
        })
        save_config(config)
        typer.echo(f"Successfully logged in as user {user_id}")
    except Exception as e:
        typer.echo(f"Login failed: {str(e)}", err=True)
        raise typer.Exit(1)

@auth_app.command("logout")
def logout():
    """Logout from Felafax"""
    config = load_config()
    
    if not config.get("token"):
        typer.echo("Not logged in.")
        return
    
    config.pop("token", None)
    config.pop("user_id", None)
    save_config(config)
    typer.echo("Successfully logged out") 