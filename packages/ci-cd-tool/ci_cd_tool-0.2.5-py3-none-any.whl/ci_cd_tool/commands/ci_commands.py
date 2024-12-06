import click
from ..core.container import Container
from ..core.exceptions import error_handler
from ..services.test_service import TestConfig

@click.group(name='ci')
def ci_group():
    """CI 파이프라인 관련 명령어"""
    pass

@ci_group.command(name='test')
@click.option('--env', type=str, default='staging', help="테스트 실행 환경 설정")
@click.option('--fast', is_flag=True, help="빠른 테스트 모드로 일부 테스트만 실행")
@click.option('--report', is_flag=True, help="테스트 결과 리포트를 생성")
@error_handler()
def test(env: str, fast: bool, report: bool):
    """테스트 실행"""
    container = Container()
    test_service = container.test_service()
    test_config = TestConfig(env=env, fast=fast, report=report)
    test_service.run_tests(test_config)

@ci_group.command(name='status')
@click.option('--env', type=str, default='prod', help="상태를 확인할 환경 설정")
@click.option('--details', is_flag=True, help="상세 정보 표시")
@click.option('--limit', type=int, help="표시할 파이프라인 수 제한")
@error_handler()
def status(env: str, details: bool, limit: int):
    """파이프라인 상태 확인"""
    container = Container()
    status_service = container.status_service()
    status_service.show_status(env, details, limit) 