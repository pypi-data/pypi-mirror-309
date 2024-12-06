import click
import yaml
import os
from src.ci_cd_tool.ci import git_setting

# 템플릿 경로
TEMPLATES_PATH = "ci_cd_tool/templates/templates"

# 기본 템플릿 정의
DEFAULT_TEMPLATES = {
    "github_actions": {
        "name": "CI Pipeline",
        "on": ["push"],
        "jobs": {
            "build": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v2"},
                    {"name": "Set up Python", "uses": "actions/setup-python@v2", "with": {"python-version": "3.x"}},
                    {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                    {"name": "Run tests", "run": "pytest"},
                ],
            }
        }
    },
    "gitlab_ci": {
        "stages": ["build", "test", "deploy"],
        "build": {
            "stage": "build",
            "script": ["echo Building..."]
        },
        "test": {
            "stage": "test",
            "script": ["pytest"]
        },
        "deploy": {
            "stage": "deploy",
            "script": ["echo Deploying..."]
        }
    },
    "jenkins": {
        "pipeline": {
            "stages": [
                {"stage": "Build", "steps": ["echo Building..."]},
                {"stage": "Test", "steps": ["pytest"]},
                {"stage": "Deploy", "steps": ["echo Deploying..."]}
            ]
        }
    }
}

# CI 템플릿 생성 함수
def generate_ci_template(ci_tool, config_data):
    """사용자가 선택한 CI 도구에 맞는 템플릿을 생성"""
    template_file = os.path.join(TEMPLATES_PATH, f"{ci_tool.lower()}.yml")
    click.echo(f"템플릿 파일 경로: {template_file}")
    if not os.path.exists(template_file):
        click.echo(f"{ci_tool} CI 템플릿 파일이 존재하지 않습니다.")
        click.echo("기본 템플릿을 생성합니다.")
        # 기본 템플릿 생성
        default_template_content = {
            'name': f"{ci_tool} CI Pipeline",
            'on': ['push', 'pull_request'],
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {'name': 'Checkout code', 'uses': 'actions/checkout@v2'},
                        {'name': 'Set up Python', 'uses': 'actions/setup-python@v2', 'with': {'python-version': '3.x'}},
                        {'name': 'Install dependencies', 'run': 'pip install -r requirements.txt'},
                        {'name': 'Run tests', 'run': 'pytest'}
                    ]
                }
            }
        }

        with open(template_file, 'w') as file:
            yaml.dump(default_template_content, file, default_flow_style=False)

        click.echo(f"기본 {ci_tool} CI 템플릿 파일이 생성되었습니다: {template_file}")

    # 템플릿 파일 로드 및 수정
    with open(template_file, 'r') as file:
        template_content = yaml.safe_load(file)

    # 설정값 반영
    if ci_tool == "GitHub Actions":
        template_content['jobs']['build']['steps'][1]['with']['python-version'] = config_data.get('python_version', '3.x')
        template_content['jobs']['build']['steps'][2]['run'] = f"pytest --version={config_data.get('test_framework', 'pytest')}"

    # 최종 템플릿 파일을 프로젝트 루트에 저장
    project_root = config_data.get('Project_Root', '.')
    output_file = os.path.join(project_root, f".github/workflows/{ci_tool.lower()}_ci.yml")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as output:
        yaml.dump(template_content, output, default_flow_style=False)
    
    click.echo(f"CI 템플릿 파일이 생성되었습니다: {output_file}")
    
    # Git 설정 및 커밋
    git_setting.commit_and_push_template(ci_tool, output_file)

