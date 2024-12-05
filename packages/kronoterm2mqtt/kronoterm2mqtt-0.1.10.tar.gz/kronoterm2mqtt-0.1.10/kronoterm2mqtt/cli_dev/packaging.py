import sys
from pathlib import Path

from cli_base.cli_tools.dev_tools import run_unittest_cli
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from manageprojects.utilities.publish import publish_package

import kronoterm2mqtt
from kronoterm2mqtt.cli_dev import PACKAGE_ROOT, cli


@cli.command()
def install():
    """
    Run pip-sync and install 'cli_base' via pip as editable.
    """
    verbose_check_call('pip-sync', PACKAGE_ROOT / 'requirements.dev.txt')
    verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


def _call_safety():
    """
    Run safety check against current requirements files
    """
    verbose_check_call(
        'safety',
        'check',
        '--ignore',
        '70612',  # Jinja2 Server Side Template Injection (SSTI)
        '--ignore',
        '73725', # starlette DoS 
        '-r',
        'requirements.dev.txt',
    )


@cli.command()
def safety():
    """
    Run safety check against current requirements files
    """
    _call_safety()


@cli.command()
def update():
    """
    Update "requirements*.txt" dependencies files
    """
    bin_path = Path(sys.executable).parent

    verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip')
    verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip-tools')

    extra_env = dict(
        CUSTOM_COMPILE_COMMAND='./dev-cli.py update',
    )

    pip_compile_base = [
        bin_path / 'pip-compile',
        '--verbose',
        '--allow-unsafe',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--resolver=backtracking',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--upgrade',
        '--generate-hashes',
    ]

    # Only "prod" dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--output-file',
        'requirements.txt',
        extra_env=extra_env,
        timeout=5000,
    )

    # dependencies + "dev"-optional-dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--extra=dev',
        '--output-file',
        'requirements.dev.txt',
        extra_env=extra_env,
        timeout=5000,
    )

    _call_safety()  # Check new dependencies for known security issues

    # Install new dependencies in current .venv:
    verbose_check_call(bin_path / 'pip-sync', 'requirements.dev.txt')


@cli.command()
def publish():
    """
    Build and upload this project to PyPi
    """
    run_unittest_cli(verbose=False, exit_after_run=False)  # Don't publish a broken state

    publish_package(
        module=kronoterm2mqtt,
        package_path=PACKAGE_ROOT,
    )
