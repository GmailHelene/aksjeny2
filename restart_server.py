#!/usr/bin/env python3
"""Restart Flask development server"""
import os
import signal
import psutil
import sys
import time

def kill_flask():
    """Kill existing Flask server process"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'python3' in proc.info['cmdline'][0] and 'main.py' in proc.info['cmdline']:
                print(f"Stopping Flask server (PID: {proc.info['pid']})")
                os.kill(proc.info['pid'], signal.SIGTERM)
                time.sleep(1)  # Give it time to shutdown gracefully
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == '__main__':
    kill_flask()
    print("Starting new Flask server...")
    os.execv(sys.executable, ['python3', 'main.py'])
