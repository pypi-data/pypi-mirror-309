from dataclasses import dataclass
from typing import Optional
import boto3
from rich.console import Console
from rich.panel import Panel
from .base_deployer import BaseDeployer

@dataclass
class AWSDeployConfig:
    region: str
    instance_type: str
    ami_id: str
    bucket_name: Optional[str] = None
    
class AWSDeployer(BaseDeployer):
    def __init__(self, config: AWSDeployConfig):
        super().__init__()
        self.config = config
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