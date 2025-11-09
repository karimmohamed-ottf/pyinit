# Copyright (c) 2025 mrbooo895.
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
Small Function for handling Ctrl+C/Ctrl+D Intterupts
"""

import sys

from rich.console import Console

console = Console()


def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (KeyboardInterrupt, EOFError):
            console.print("[red]\n-> [ERROR] Interrupted By The User")
            sys.exit(1)
        except Exception as e:
            # A general catch-all for other potential issues (e.g., file permissions).
            console.print(f"[bold red][ERROR][/bold red] -> {e}")
            sys.exit(1)

    return wrapper
