import click
from rich.console import Console
from ..services.initialization_service import InitializationService

@click.command(help="CI/CD 기본설정 및 초기화")
def cc_init():
    console = Console()
    service = InitializationService(console)
    
    if service.initialize():
        console.print("[green]초기화가 완료되었습니다![/green]")
    else:
        console.print("[red]초기화가 실패했습니다.[/red]")