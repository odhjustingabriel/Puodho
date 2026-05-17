#!/usr/bin/env python
import importlib.util
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puodho_farm.settings')
    if importlib.util.find_spec('django') is None:
        sys.stderr.write(
            "Django is not installed in this Python environment.\n\n"
            "Install the project dependencies, then run the command again:\n"
            "  python -m pip install -r requirements.txt\n\n"
            "If you are using a virtual environment, activate it first.\n"
            "Windows PowerShell example:\n"
            "  .\\.venv\\Scripts\\Activate.ps1\n"
            "  python -m pip install -r requirements.txt\n"
        )
        sys.exit(1)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
