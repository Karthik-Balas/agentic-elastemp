"""CLI and packaging smoke tests."""

import subprocess
import sys

import pytest

import elastemp
from elastemp.cli import OPERATIONS, main


def test_version_is_exposed():
    assert isinstance(elastemp.__version__, str) and elastemp.__version__


def test_help_lists_all_operations(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert all(op in out for op in OPERATIONS)


def test_missing_input_gives_nonzero_exit(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["--operations", "get_elastic", "--log-file", ""]) == 1


def test_make_elastic_without_poscar_fails_cleanly(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["--operations", "make_elastic", "--log-file", ""]) == 1


def test_python_dash_m_entry_point():
    result = subprocess.run([sys.executable, "-m", "elastemp", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "--operations" in result.stdout
