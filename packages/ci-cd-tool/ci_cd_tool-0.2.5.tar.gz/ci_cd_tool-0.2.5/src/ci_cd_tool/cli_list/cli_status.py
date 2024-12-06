import click
from rich.console import Console
from rich.panel import Panel
from ..config.config_manager import ConfigurationManager
from ..services.github_service import GitHubService
from ..services.status_service import StatusDisplayService
from ..core.monitoring import MonitoringService, PipelineStatus

@click.command(help="파이프라인 상태 확인")
@click.option('--env', default='dev', help="환경 설정 (예: dev, staging, prod)")
@click.option('--limit', default=5, help="표시할 파이프라인 실행 수")
@click.option('--details', is_flag=True, help="상세 정보 표시")
def cli_status(env: str, limit: int, details: bool):
    console = Console()
    config_manager = ConfigurationManager()
    monitoring_service = MonitoringService()
    
    try:
        config = config_manager.load()
        github_service = GitHubService(
            config.ci_cd_base_url,
            config.ci_cd_token,
            config.repo_owner,
            config.repo_name
        )
        
        pipeline_runs = github_service.get_pipeline_runs(
            branch=config.environments[env]['branch'],
            limit=limit
        )
        
        for run in pipeline_runs:
            status = PipelineStatus(
                pipeline_id=str(run['id']),
                name=run['name'],
                status=run['status'],
                created_at=run['created_at'],
                conclusion=run['conclusion'],
                url=run['url']
            )
            monitoring_service.update_pipeline_status(status)
        
        monitoring_service.display_status()
            
    except Exception as e:
        console.print(Panel(f"[red]오류 발생: {str(e)}[/red]", 
                          title="오류", border_style="red"))
