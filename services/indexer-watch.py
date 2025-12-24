#!/usr/bin/env python3
"""
Indexer Watch Service - Watches for JSONL changes and re-indexes

Runs as a daemon/service, watching Claude Code session files for changes.
When a session file is modified, re-indexes that repo and updates YAML.

Cross-platform: Works on Windows, Linux, and WSL.

Usage:
    python indexer-watch.py          # Run in foreground
    python indexer-watch.py --daemon # Run as background process (Linux/WSL only)
    python indexer-watch.py --stop   # Stop running daemon
    python indexer-watch.py --status # Check daemon status
"""

import os
import sys
import time
import signal
import subprocess
import threading
import platform
from pathlib import Path
from datetime import datetime

# Import from shared config
from config import (
    CLAUDE_PROJECTS,
    SERVICES_DIR,
    STATE_FILE,
    LOG_FILE,
    PID_FILE,
    POLL_INTERVAL,
)

IS_WINDOWS = platform.system() == "Windows"

# Track file modification times
file_mtimes = {}
running = True


def log(msg: str):
    """Log with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + "\n")
    except:
        pass


def get_jsonl_files():
    """Get all JSONL session files with their modification times."""
    files = {}
    if not CLAUDE_PROJECTS.exists():
        return files

    for project_dir in CLAUDE_PROJECTS.iterdir():
        if not project_dir.is_dir():
            continue
        # JSONL files are stored directly in project folder
        for jsonl_file in project_dir.glob("*.jsonl"):
            # Skip agent transcripts
            if "agent-" in jsonl_file.name:
                continue
            try:
                mtime = jsonl_file.stat().st_mtime
                files[str(jsonl_file)] = mtime
            except:
                pass
    return files


def check_for_changes():
    """Check if any JSONL files have changed."""
    global file_mtimes

    current_files = get_jsonl_files()
    changed = False

    for path, mtime in current_files.items():
        if path not in file_mtimes:
            # New file
            log(f"New session: {Path(path).name}")
            changed = True
        elif file_mtimes[path] < mtime:
            # Modified file
            log(f"Modified: {Path(path).name}")
            changed = True

    file_mtimes = current_files
    return changed


def run_indexer():
    """Run the conversation indexer."""
    log("Running indexer...")
    try:
        indexer_script = Path(__file__).parent / "conversation-indexer.py"
        result = subprocess.run(
            [sys.executable, str(indexer_script)],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes
            cwd=str(Path(__file__).parent)
        )
        # Count created files from output
        lines = result.stdout.split('\n')
        indexed = sum(1 for l in lines if 'Index:' in l)
        log(f"Indexer complete: {indexed} indexes updated")
        if result.returncode != 0 and result.stderr:
            log(f"Indexer stderr: {result.stderr[:200]}")
        return True
    except subprocess.TimeoutExpired:
        log("Indexer timed out")
        return False
    except Exception as e:
        log(f"Indexer error: {e}")
        return False


def cleanup(signum=None, frame=None):
    """Clean up on exit."""
    global running
    running = False
    log("Shutting down...")
    if PID_FILE.exists():
        try:
            PID_FILE.unlink()
        except:
            pass
    sys.exit(0)


def write_pid():
    """Write PID file."""
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))


def is_process_running(pid: int) -> bool:
    """Check if a process with the given PID is running."""
    if IS_WINDOWS:
        try:
            # Windows: use tasklist
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}', '/NH'],
                capture_output=True,
                text=True
            )
            return str(pid) in result.stdout
        except:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False


def stop_daemon():
    """Stop the running daemon."""
    if not PID_FILE.exists():
        print("Not running")
        return

    pid = int(PID_FILE.read_text().strip())

    if IS_WINDOWS:
        try:
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
            print(f"Stopped (PID: {pid})")
        except:
            print("Failed to stop")
    else:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Stopped (PID: {pid})")
        except ProcessLookupError:
            print("Not running")

    try:
        PID_FILE.unlink()
    except:
        pass


def check_status():
    """Check daemon status."""
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        if is_process_running(pid):
            print(f"Running (PID: {pid})")
        else:
            print("Not running (stale PID file)")
            PID_FILE.unlink()
    else:
        print("Not running")


def daemonize_unix():
    """Fork into background (Unix/Linux only)."""
    # First fork
    pid = os.fork()
    if pid > 0:
        print(f"Indexer watch started (PID: {pid})")
        print(f"Log: {LOG_FILE}")
        sys.exit(0)

    # Decouple from parent
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # Second fork
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    # Redirect stdio
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    with open(LOG_FILE, 'a') as logfile:
        os.dup2(logfile.fileno(), sys.stdout.fileno())
        os.dup2(logfile.fileno(), sys.stderr.fileno())


def daemonize_windows():
    """Start as background process (Windows)."""
    # On Windows, we use subprocess to start a detached process
    script_path = Path(__file__).resolve()

    # Start a new process with CREATE_NO_WINDOW flag
    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008

    subprocess.Popen(
        [sys.executable, str(script_path), '--background'],
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
        stdout=open(LOG_FILE, 'a'),
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        cwd=str(script_path.parent)
    )
    print(f"Indexer watch started in background")
    print(f"Log: {LOG_FILE}")
    sys.exit(0)


def watch_loop():
    """Main watch loop."""
    global running

    write_pid()
    log("Indexer watch started")
    log(f"Watching: {CLAUDE_PROJECTS}")
    log(f"Check interval: {POLL_INTERVAL}s")

    # Initial index
    file_mtimes.update(get_jsonl_files())
    run_indexer()

    # Watch loop
    while running:
        time.sleep(POLL_INTERVAL)
        if check_for_changes():
            run_indexer()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Indexer Watch Service")
    parser.add_argument("--daemon", "-d", action="store_true", help="Run as daemon/background process")
    parser.add_argument("--background", action="store_true", help="Internal flag for Windows background mode")
    parser.add_argument("--stop", action="store_true", help="Stop running daemon")
    parser.add_argument("--status", action="store_true", help="Check daemon status")
    args = parser.parse_args()

    if args.status:
        check_status()
        return

    if args.stop:
        stop_daemon()
        return

    # Check if already running
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        if is_process_running(pid):
            print(f"Already running (PID: {pid})")
            return
        else:
            PID_FILE.unlink()

    if args.daemon and not args.background:
        if IS_WINDOWS:
            daemonize_windows()
        else:
            daemonize_unix()

    # Set up signal handlers
    if not IS_WINDOWS:
        signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    watch_loop()


if __name__ == "__main__":
    main()
