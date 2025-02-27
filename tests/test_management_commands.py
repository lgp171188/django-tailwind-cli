import sys
from pathlib import Path
from typing import Any

import pytest
from django.conf import LazySettings
from django.core.management import CommandError, call_command
from pytest_mock import MockerFixture

from django_tailwind_cli.management.commands.tailwind import DEFAULT_TAILWIND_CONFIG
from django_tailwind_cli.management.commands.tailwind import Command as TailwindCommand
from django_tailwind_cli.utils import Config


@pytest.fixture(autouse=True)
def configure_settings(mocker: MockerFixture):
    mocker.resetall()
    mocker.patch("multiprocessing.Process.start")
    mocker.patch("multiprocessing.Process.join")
    mocker.patch("subprocess.run")
    mocker.patch("urllib.request.urlopen")
    mocker.patch("shutil.copyfileobj")


def test_calling_unknown_subcommand():
    with pytest.raises(CommandError, match="invalid choice: 'not_a_valid_command'"):
        call_command("tailwind", "not_a_valid_command")


def test_invalid_configuration(settings: LazySettings):
    settings.STATICFILES_DIRS = None
    with pytest.raises(CommandError, match="Configuration error"):
        call_command("tailwind", "build")

    settings.STATICFILES_DIRS = []
    with pytest.raises(CommandError, match="Configuration error"):
        call_command("tailwind", "build")


def test_download_cli(settings: LazySettings, tmp_path: Path, config: Config):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    assert not config.get_full_cli_path().exists()
    call_command("tailwind", "build")
    assert config.get_full_cli_path().exists()


def test_download_cli_without_tailwind_cli_path(
    settings: LazySettings, tmp_path: Path, config: Config
):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = None
    assert not config.get_full_cli_path().exists()
    call_command("tailwind", "build")
    assert config.get_full_cli_path().exists()


def test_create_tailwind_config_if_non_exists(
    settings: LazySettings, tmp_path: Path, config: Config
):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    assert not config.get_full_config_file_path().exists()
    call_command("tailwind", "build")
    assert config.get_full_cli_path().exists()
    assert DEFAULT_TAILWIND_CONFIG == config.get_full_config_file_path().read_text()


def test_with_existing_tailwind_config(settings: LazySettings, tmp_path: Path, config: Config):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    config.get_full_config_file_path().write_text("module.exports = {}")
    call_command("tailwind", "build")
    assert config.get_full_config_file_path().exists()
    assert "module.exports = {}" == config.get_full_config_file_path().read_text()
    assert DEFAULT_TAILWIND_CONFIG != config.get_full_config_file_path().read_text()


def test_build_subprocess_run_called(settings: LazySettings, tmp_path: Path, mocker: MockerFixture):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    subprocess_run = mocker.patch("subprocess.run")
    call_command("tailwind", "build")
    assert 1 <= subprocess_run.call_count <= 2


def test_build_output_of_first_run(settings: LazySettings, tmp_path: Path, capsys: Any):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    call_command("tailwind", "build")
    captured = capsys.readouterr()
    assert "Tailwind CSS CLI not found." in captured.out
    assert "Downloading Tailwind CSS CLI from " in captured.out
    assert "Built production stylesheet" in captured.out


def test_build_output_of_second_run(settings: LazySettings, tmp_path: Path, capsys: Any):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    call_command("tailwind", "build")
    captured = capsys.readouterr()
    call_command("tailwind", "build")
    captured = capsys.readouterr()
    assert "Tailwind CSS CLI not found." not in captured.out
    assert "Downloading Tailwind CSS CLI from " not in captured.out
    assert "Built production stylesheet" in captured.out


@pytest.mark.skipif(
    sys.version_info < (3, 9),
    reason="The capturing of KeyboardInterupt fails with pytest every other time.",
)
def test_build_keyboard_interrupt(
    settings: LazySettings, tmp_path: Path, mocker: MockerFixture, capsys: Any
):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.side_effect = KeyboardInterrupt
    call_command("tailwind", "build")
    captured = capsys.readouterr()
    assert "Canceled building production stylesheet." in captured.out


def test_get_build_cmd(settings: LazySettings):
    assert "--input" not in TailwindCommand().get_build_cmd()
    settings.TAILWIND_CLI_SRC_CSS = "css/source.css"
    assert "--input" in TailwindCommand().get_build_cmd()


def test_watch_subprocess_run_called(settings: LazySettings, tmp_path: Path, mocker: MockerFixture):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    subprocess_run = mocker.patch("subprocess.run")
    call_command("tailwind", "watch")
    assert 1 <= subprocess_run.call_count <= 2


def test_watch_output_of_first_run(settings: LazySettings, tmp_path: Path, capsys: Any):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    call_command("tailwind", "watch")
    captured = capsys.readouterr()
    assert "Tailwind CSS CLI not found." in captured.out
    assert "Downloading Tailwind CSS CLI from " in captured.out


def test_watch_output_of_second_run(settings: LazySettings, tmp_path: Path, capsys: Any):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    call_command("tailwind", "watch")
    captured = capsys.readouterr()
    call_command("tailwind", "watch")
    captured = capsys.readouterr()
    assert "Tailwind CSS CLI not found." not in captured.out
    assert "Downloading Tailwind CSS CLI from " not in captured.out


@pytest.mark.skipif(
    sys.version_info < (3, 9),
    reason="The capturing of KeyboardInterupt fails with pytest every other time.",
)
def test_watch_keyboard_interrupt(
    settings: LazySettings, tmp_path: Path, mocker: MockerFixture, capsys: Any
):
    settings.BASE_DIR = tmp_path
    settings.TAILWIND_CLI_PATH = str(tmp_path)
    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.side_effect = KeyboardInterrupt
    call_command("tailwind", "watch")
    captured = capsys.readouterr()
    assert "Stopped watching for changes." in captured.out


def test_get_watch_cmd(settings: LazySettings):
    assert "--input" not in TailwindCommand().get_watch_cmd()
    settings.TAILWIND_CLI_SRC_CSS = "css/source.css"
    assert "--input" in TailwindCommand().get_watch_cmd()


def test_runserver():
    call_command("tailwind", "runserver")


def test_runserver_plus_with_django_extensions_installed():
    call_command("tailwind", "runserver_plus")


def test_runserver_plus_without_django_extensions_installed(mocker: Any):
    mocker.patch.dict(sys.modules, {"django_extensions": None})
    with pytest.raises(CommandError, match="Missing dependencies."):
        call_command("tailwind", "runserver_plus")


def test_list_project_templates(capsys: Any):
    call_command("tailwind", "list_templates")
    captured = capsys.readouterr()
    assert "templates/tailwind_cli/base.html" in captured.out
    assert "templates/tailwind_cli/tailwind_css.html" in captured.out
    assert "templates/tests/base.html" in captured.out
    assert "templates/admin" not in captured.out


def test_list_projecttest_list_project_all_templates_templates(capsys: Any, settings: LazySettings):
    settings.INSTALLED_APPS = [
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.auth",
        "django.contrib.admin",
        "django.contrib.staticfiles",
        "django_tailwind_cli",
    ]
    call_command("tailwind", "list_templates")
    captured = capsys.readouterr()
    assert "templates/tailwind_cli/base.html" in captured.out
    assert "templates/tailwind_cli/tailwind_css.html" in captured.out
    assert "templates/tests/base.html" in captured.out
    assert "templates/admin" in captured.out
