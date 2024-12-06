import click
from rich.console import Console
from ..services.test_service import TestService, TestConfig
from ..services.github_actions_service import GitHubActionsService
from ..config.config_manager import ConfigurationManager

@click.command(help="CI/CD 파이프라인에서 테스트 실행")
@click.option('--env', type=str, default='staging', help="테스트 실행 환경 설정")
@click.option('--fast', is_flag=True, help="빠른 테스트 모드로 일부 테스트만 실행")
@click.option('--report', is_flag=True, help="테스트 결과 리포트를 생성")
def cli_test(env: str, fast: bool, report: bool):
    console = Console()
    config_manager = ConfigurationManager()
    
    test_service = TestService(console)
    test_config = TestConfig(env=env, fast=fast, report=report)
    
    if test_service.run_tests(test_config):
        github_actions = GitHubActionsService(console, config_manager)
        github_actions.add_test_configuration(fast, report)