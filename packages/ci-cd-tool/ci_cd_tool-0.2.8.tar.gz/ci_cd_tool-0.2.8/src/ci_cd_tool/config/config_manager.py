import yaml  # PyYAML 라이브러리
import os
import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from .configuration import Configuration

# 설정 파일 경로
# CONFIG_FILE = "ci_cd_tool/config/config_test.yml"
CONFIG_FILE = "ci_cd_tool/config/config.yml"
console = Console()


class ConfigurationManager:
    def __init__(self, config_file: str = "ci_cd_tool/config/config.yml"):
        self.config_file = Path(config_file)
        self.console = Console()
        self._config = None

    def load(self) -> Configuration:
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config_dict = yaml.safe_load(f)
                self._config = Configuration.from_dict(config_dict)
                return self._config
        return Configuration.from_dict({})

    def save(self, config: Configuration):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(config.to_dict(), f)

    def show(self):
        config = self.load()
        if config:
            config_text = "\n".join(
                f"[bold]{k}:[/bold] {v}" 
                for k, v in config.to_dict().items()
            )
            self.console.print(Panel(
                config_text,
                title="[green bold]Config 설정 정보[/]",
                border_style="green"
            ))


# 설정 파일 값 변경 기능
def change_config(key, value):
    """설정 파일의 특정 값을 변경"""
    config_manager = ConfigurationManager()
    config = config_manager.load()
    config_dict = config.to_dict()
    config_dict[key] = value
    config_manager.save(Configuration.from_dict(config_dict))
    click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")


# 설정 파일 초기화 기능
def reset_config():
    """설정 파일 초기화"""
    config_manager = ConfigurationManager()
    config_manager.save(Configuration.from_dict({}))
    click.echo(f"{CONFIG_FILE} 파일이 초기화되었습니다.")