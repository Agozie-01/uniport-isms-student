#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import webbrowser
import threading
import time

def open_browser():
    # Wait briefly to ensure the server has started before attempting to open the browser
    time.sleep(1)  # Adjust delay as needed for the server to be ready
    webbrowser.open("http://127.0.0.1:12000")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isms_admin.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Default to running server on 0.0.0.0:12000 if no arguments provided
    if len(sys.argv) == 1:
        sys.argv += ["runserver", "0.0.0.0:12000"]

    # If running server, add '--noreload' to avoid autoreload
    if 'runserver' in sys.argv:
        sys.argv.append('--noreload')
        # Start a thread to open the browser so it does not block the server from starting
        threading.Thread(target=open_browser, daemon=True).start()
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
