import click
from ..core.container import Container
from ..core.exceptions import error_handler
from ..core.plugin import PluginManager
from ci_cd_tool.core.commands.deploy_commands import DeployCommand
from dataclasses import dataclass
from typing import Optional
from rich.console import Console
from rich.panel import Panel
import boto3

@click.group(name='cd')
def cd_group():
    """CD 파이프라인 관련 명령어"""
    pass

@cd_group.command(name='deploy')
@click.option('--env', type=str, default='dev', help="배포할 환경 설정")
@error_handler()
def deploy(env: str):
    """환경별 배포 실행"""
    container = Container()
    deploy_service = container.deploy_service()
    deploy_service.deploy(env)

@cd_group.command(name='rollback')
@click.option('--version', type=str, required=True, help="롤백할 버전")
@click.option('--force', is_flag=True, help="강제 롤백")
@error_handler()
def rollback(version: str, force: bool):
    """특정 버전으로 롤백"""
    container = Container()
    deploy_service = container.deploy_service()
    deploy_service.rollback(version, force)

@dataclass
class AWSDeployConfig:
    region: str
    instance_type: str
    ami_id: str
    bucket_name: Optional[str] = None
    
class AWSDeployer:
    def __init__(self, config: AWSDeployConfig):
        self.config = config
        self.console = Console()
        self.ec2 = boto3.resource('ec2', region_name=config.region)
        self.s3 = boto3.client('s3', region_name=config.region)
    
    def deploy(self):
        try:
            instance = self._create_instance()
            if self.config.bucket_name:
                self._upload_artifacts()
            return True
        except Exception as e:
            self.console.print(Panel(f"[red]배포 실패: {str(e)}[/red]", 
                                  title="오류", border_style="red"))
            return False
            
    def _create_instance(self):
        self.console.print("[yellow]EC2 인스턴스 생성 중...[/yellow]")
        return self.ec2.create_instances(
            ImageId=self.config.ami_id,
            InstanceType=self.config.instance_type,
            MinCount=1,
            MaxCount=1
        )[0]
        
    def _upload_artifacts(self):
        self.console.print("[yellow]아티팩트 업로드 중...[/yellow]")
        # 아티팩트 업로드 로직 구현 