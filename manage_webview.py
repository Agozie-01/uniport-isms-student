#!/usr/bin/env python
"""Django's command-line utility for administrative tasks with pywebview for a desktop window."""
import os
import sys
import threading
import time
import webview  # pywebview to create a desktop-like window for the Django app
from django.core.management import execute_from_command_line

def start_django_server():
    """Start Django server."""
    sys.argv = [sys.argv[0], "runserver", "127.0.0.1:12000", "--noreload"]
    execute_from_command_line(sys.argv)

def main():
    """Run Django administrative tasks and launch the server in a desktop window."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isms.settings')

    # Start Django server in a background thread
    server_thread = threading.Thread(target=start_django_server, daemon=True)
    server_thread.start()

    # Wait briefly to ensure server has started before launching the window
    time.sleep(1)  # Adjust this delay if needed for server readiness

    # Open the application in a PyWebView window; when this window is closed, the app exits
    webview.create_window("ISMS", "http://127.0.0.1:12000")
    webview.start()  # Blocks until the window is closed, then exits

if __name__ == '__main__':
    main()
