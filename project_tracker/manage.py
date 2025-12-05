#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django is not installed. Create venv and pip install django.") from exc
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    main()
