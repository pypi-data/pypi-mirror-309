
import os
import webbrowser
import threading
import time

def open_html_periodically(file_path, interval=30):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    def open_file():
        while True:
            webbrowser.open(f"file://{os.path.abspath(file_path)}")
            time.sleep(interval)
    
    thread = threading.Thread(target=open_file, daemon=True)
    thread.start()
