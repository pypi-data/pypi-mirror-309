import click
from rich.console import Console
from .commands import ci_group, cd_group, config_group, monitor_group
from .core.logging import setup_logging

@click.group()
@click.version_option(version='1.0.0')
def main():
    """CI/CD 도구 CLI"""
    setup_logging()

# 명령어 그룹 등록
main.add_command(ci_group)
main.add_command(cd_group)
main.add_command(config_group)
main.add_command(monitor_group)

if __name__ == '__main__':
    main()
