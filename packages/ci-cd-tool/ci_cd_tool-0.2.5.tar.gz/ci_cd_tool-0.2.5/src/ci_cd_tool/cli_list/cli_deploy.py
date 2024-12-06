import click
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from rich.console import Console
from rich.panel import Panel

console = Console()

class AWSDeployer:
    def __init__(self, region_name):
        self.region_name = region_name
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)

    def upload_to_s3(self, bucket_name, file_path, s3_key):
        """S3에 파일 업로드"""
        console.print(Panel(f"[yellow]S3 버킷 {bucket_name}에 파일 {file_path} 업로드 중...[/yellow]", 
                          title="S3 업로드", border_style="yellow"))
        self.s3_client.upload_file(file_path, bucket_name, s3_key)
        console.print(Panel("[green]파일 업로드 완료[/green]", 
                          title="업로드 결과", border_style="green"))

    def create_ec2_instance(self, instance_type, ami_id):
        """EC2 인스턴스 생성"""
        console.print(Panel("[yellow]EC2 인스턴스 생성 중...[/yellow]", 
                          title="EC2 생성", border_style="yellow"))
        instance = self.ec2_resource.create_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1
        )
        console.print(Panel(f"[green]EC2 인스턴스 생성 완료: ID {instance[0].id}[/green]", 
                          title="EC2 결과", border_style="green"))
        return instance[0]

class DeploymentManager:
    def __init__(self, env):
        self.env = env
        console.print(Panel(f"[blue]{env} 환경으로 배포 중...[/blue]", 
                          title="배포 진행", border_style="blue"))

    def handle_aws_error(self, error):
        """AWS 관련 에러 처리"""
        if isinstance(error, NoCredentialsError):
            console.print(Panel("[red]AWS 자격 증명이 올바르지 않습니다. 환경 변수를 확인해주세요.[/red]", 
                              title="오류", border_style="red"))
        elif isinstance(error, ClientError):
            error_code = error.response['Error']['Code']
            if error_code == 'AccessDenied':
                console.print(Panel("[red]접근이 거부되었습니다. 권한을 확인하세요.[/red]", 
                                  title="오류", border_style="red"))
            elif error_code == 'NoSuchBucket':
                console.print(Panel("[red]지정한 S3 버킷이 존재하지 않습니다. 버킷 이름을 확인하세요.[/red]", 
                                  title="오류", border_style="red"))
            else:
                console.print(Panel(f"[red]AWS 클라이언트 오류: {str(error)}[/red]", 
                                  title="오류", border_style="red"))

    def get_deployment_inputs(self):
        """사용자로부터 배포 관련 입력 받기"""
        region_name = click.prompt("AWS Region", default='us-east-1')
        bucket_name = click.prompt("S3 버킷 이름", type=str)
        file_path = click.prompt("업로드할 파일 경로", type=str)
        s3_key = click.prompt("S3에 저장할 파일 키", type=str)
        instance_type = click.prompt("EC2 인스턴스 타입", default='t2.micro')
        ami_id = click.prompt("AMI ID", default='ami-042e8287309f5df03')
        
        return {
            'region_name': region_name,
            'bucket_name': bucket_name,
            'file_path': file_path,
            's3_key': s3_key,
            'instance_type': instance_type,
            'ami_id': ami_id
        }