"""Nox configuration."""

from __future__ import annotations

from pathlib import Path

import nox

nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv"
nox.options.reuse_venv = "yes"

package = "tap-pulumi-cloud"
src_dir = "tap_pulumi_cloud"
tests_dir = "tests"

PYPROJECT = nox.project.load_toml()
python_versions = nox.project.python_versions(PYPROJECT)
main_python = Path(".python-version").read_text(encoding="utf-8").rstrip()
locations = src_dir, tests_dir, "noxfile.py"
nox.options.sessions = ("tests",)


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Execute pytest tests and compute coverage."""
    session.run_install(
        "uv",
        "sync",
        "--locked",
        "--no-dev",
        "--group=test",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
            "UV_PYTHON": session.python,
        },
    )

    session.run("pytest", *session.posargs)
