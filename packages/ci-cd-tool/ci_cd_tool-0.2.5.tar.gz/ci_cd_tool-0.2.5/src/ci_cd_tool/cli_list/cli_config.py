from dataclasses import dataclass
from typing import Optional, Dict, Any
import inquirer
import click
from ci_cd_tool.config.config_manager import load_config, show_config, change_config, reset_config
from ci_cd_tool.utils.cli_prompt import set_top_screen

class ConfigManager:
    def __init__(self):
        self.config_data = load_config()

    def show_settings(self):
        """설정 파일 조회"""
        show_config()

    def change_setting(self, key: str, value: str):
        """설정 값 변경: 명령어 기반"""
        change_config(key, value)
        click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")

    def interactive_settings(self):
        """설정 값 변경: 선택 기반"""
        set_top_screen()
        answers = self._get_user_selections()
        if answers:
            self._update_settings(answers)
            click.echo("설정 값이 변경되었습니다.")

    def _get_user_selections(self) -> Dict[str, Any]:
        """사용자 선택지 프롬프트 표시"""
        questions = [
            inquirer.List(
                'Framework',
                message="어떤 테스트 프레임워크를 사용할까요?",
                choices=['unittest', 'pytest']
            ),
            inquirer.List(
                'Pipline',
                message="포함할 파이프라인 단계를 선택하세요",
                choices=['build', 'test', 'deploy']
            )
        ]
        return inquirer.prompt(questions)

    def _update_settings(self, answers: Dict[str, Any]):
        """선택된 값으로 설정 업데이트"""
        for key, value in answers.items():
            change_config(key, value)

def cli_config_handler(show: bool, key: str = None, value: str = None, 
                      set_config: bool = False, reset: bool = False):
    """설정 파일 관리 핸들러"""
    config_manager = ConfigManager()
    
    if show:
        config_manager.show_settings()
    elif set_config and key and value:
        config_manager.change_setting(key, value)
    elif set_config:
        config_manager.interactive_settings()
    elif reset:
        reset_config()