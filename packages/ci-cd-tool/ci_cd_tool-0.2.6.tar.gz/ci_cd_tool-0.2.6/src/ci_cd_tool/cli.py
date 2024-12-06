import click
from rich.console import Console
from .commands import ci_group, cd_group, config_group
from .core.logging import setup_logging

@click.group()
@click.version_option(version="1.0.0")
def main():
    """CI/CD 도구 CLI"""
    setup_logging()

main.add_command(ci_group, name='ci')
main.add_command(cd_group, name='cd')
main.add_command(config_group, name='config')

if __name__ == "__main__":
    main()
