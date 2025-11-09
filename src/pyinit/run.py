# Copyright (c) 2025 mrbooo895.
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Implements the 'run' command for the pyinit command-line tool.

This module is responsible for executing the main entry point of a project.
It abstracts away the need for the user to manually activate the virtual
environment and find the path to the main script. It also supports passing
command-line arguments directly to the user's script.
"""

import subprocess
import sys

from rich.console import Console

from .utils import (
    check_platform,
    check_project_root,
    check_venv_exists,
    find_project_root,
    get_project_name,
)
from .wrappers import error_handling

console = Console()


@error_handling
def run_project(app_args: list = None):
    """
    Executes the project's main script within its virtual environment.

    This function serves as the entry point for the 'pyinit run' command.
    It locates the project, its virtual environment, and its main script
    (assumed to be `src/<package_name>/main.py`), and then runs it as a
    subprocess, passing along any extra arguments.

    :param list, optional app_args: A list of command-line arguments to pass
                                    to the user's script. Defaults to None.
    :raises SystemExit: If not run within a valid project or if critical files
                        (like the main script or venv) are missing.
    """
    project_root = find_project_root()
    if not app_args:
        app_args = []

    # --- Pre-flight Checks ---
    check_project_root(project_root)
    # Determine project name and construct paths to key files/directories.
    project_name = get_project_name(project_root) or project_root.name
    main_file = project_root / "src" / project_name / "main.py"
    venv_dir = project_root / "venv"

    # Verify that the expected main script exists.
    if not main_file.exists():
        console.print(
            f"[bold red][ERROR][/bold red] Main file '{main_file}' was not found."
        )
        sys.exit(1)

    # Verify that the virtual environment exists.
    check_venv_exists(venv_dir)

    # --- Determine Platform-specific Python Executable ---
    _, python_executable = check_platform(venv_dir)

    console.print(f"[bold green]    Running[/bold green] package '{project_name}'")

    # Construct the full command, including the Python interpreter,
    # the script path, and any passthrough arguments.
    run_cmd = [str(python_executable), str(main_file)] + app_args
    # Execute the command. Output is streamed directly to the console.
    subprocess.run(run_cmd, check=True)
