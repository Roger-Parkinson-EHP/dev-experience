#!/usr/bin/env python3
"""
Platform Services Configuration

Cross-platform configuration for conversation indexer and related services.
Handles Windows vs Linux/WSL path resolution dynamically.
"""

import os
import platform
import socket
from pathlib import Path
from typing import Dict, Optional

# Machine identification
MACHINE_NAME = socket.gethostname()
IS_WINDOWS = platform.system() == "Windows"
IS_WSL = "microsoft" in platform.uname().release.lower() if not IS_WINDOWS else False

# Claude projects location
if IS_WINDOWS:
    CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"
else:
    CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"

# Service state files
SERVICES_DIR = Path.home() / ".claude" / "services"
STATE_FILE = SERVICES_DIR / "indexer-state.json"
LOG_FILE = SERVICES_DIR / "indexer-watch.log"
PID_FILE = SERVICES_DIR / "indexer-watch.pid"

# Ensure services directory exists
SERVICES_DIR.mkdir(parents=True, exist_ok=True)


def discover_repos_in_folder(folder: Path) -> Dict[str, str]:
    """
    Auto-discover git repositories in a folder.

    Looks for directories containing a .git folder.
    Returns a dict mapping repo names to their filesystem paths.
    """
    repos = {}
    if not folder.exists():
        return repos

    for item in folder.iterdir():
        if item.is_dir() and (item / ".git").exists():
            repos[item.name] = str(item)

    return repos


def get_repo_paths() -> Dict[str, str]:
    """
    Get repository paths based on platform.

    Auto-discovers git repos in standard locations.
    Returns a dict mapping repo names to their filesystem paths.
    """
    repos = {}

    if IS_WINDOWS:
        # Windows: auto-discover from GitHub folder
        github_dir = Path.home() / "Documents" / "GitHub"
        repos.update(discover_repos_in_folder(github_dir))

        # Add any additional custom paths
        custom_paths = [
            # Add more Windows paths if needed
        ]
        for path in custom_paths:
            p = Path(path)
            if p.exists():
                repos[p.name] = str(p)

    elif IS_WSL:
        # WSL: check both Windows mounts and Linux home
        wsl_folders = [
            Path("/mnt/c/EHP"),
            Path("/mnt/c/Portfolio"),
            Path.home() / "projects",
        ]
        for folder in wsl_folders:
            if folder.exists():
                if folder.name == "projects":
                    repos.update(discover_repos_in_folder(folder))
                elif (folder / ".git").exists():
                    repos[folder.name] = str(folder)

    else:
        # Native Linux: auto-discover from projects folder
        projects_dir = Path.home() / "projects"
        repos.update(discover_repos_in_folder(projects_dir))

    return repos


def get_claude_project_mapping() -> Dict[str, str]:
    """
    Map Claude project folder names to repository paths.

    Auto-discovers mappings by scanning ~/.claude/projects/ folder.

    Claude stores projects with encoded paths like:
    - "-home-roger-projects-LC" -> "/home/roger/projects/LC"
    - "C--Users-Roger-Documents-GitHub-bazel-test" -> "C:/Users/Roger/Documents/GitHub/bazel-test"
    """
    mapping = {}

    if not CLAUDE_PROJECTS.exists():
        return mapping

    for project_dir in CLAUDE_PROJECTS.iterdir():
        if not project_dir.is_dir():
            continue

        encoded_name = project_dir.name

        # Decode the path from Claude's encoding
        if IS_WINDOWS:
            # Windows format: "C--Users-Roger-Documents-GitHub-bazel-test"
            # -> "C:/Users/Roger/Documents/GitHub/bazel-test"
            # Note: C-- is the drive, then single - separates path segments
            if encoded_name.startswith("C--"):
                # Split by single dash, but keep words together
                # The pattern is: DriveLetter-- then path-segments-separated-by-single-dash
                rest = encoded_name[3:]  # Remove "C--"
                # Split on single dash that's between path segments
                # This is tricky because folder names can have dashes
                # Try to decode and check if path exists
                segments = rest.split("-")

                # Try different combinations to find valid path
                decoded = None
                for i in range(len(segments), 0, -1):
                    # Try joining segments with /
                    test_path = "C:/" + "/".join(segments[:i])
                    if Path(test_path).exists():
                        # Add remaining segments
                        if i < len(segments):
                            test_path += "/" + "-".join(segments[i:])
                        if Path(test_path).exists():
                            decoded = test_path
                            break

                # Fallback: simple replacement
                if not decoded:
                    decoded = "C:/" + rest.replace("-", "/")

                if decoded and Path(decoded).exists():
                    mapping[encoded_name] = decoded
        else:
            # Linux/WSL format: "-home-roger-projects-LC" -> "/home/roger/projects/LC"
            # or "-mnt-c-Portfolio" -> "/mnt/c/Portfolio"
            if encoded_name.startswith("-"):
                decoded = "/" + encoded_name[1:].replace("-", "/")
                # Fix common path patterns
                decoded = decoded.replace("/mnt/c/", "/mnt/c/")
                if Path(decoded).exists():
                    mapping[encoded_name] = decoded

    return mapping


def resolve_repo_from_project_name(project_name: str) -> Optional[str]:
    """
    Resolve a Claude project folder name to a repository path.

    Args:
        project_name: The encoded project folder name from ~/.claude/projects/

    Returns:
        The filesystem path to the repository, or None if not found.
    """
    mapping = get_claude_project_mapping()
    return mapping.get(project_name)


def get_repo_colors() -> Dict[str, str]:
    """Get color codes for each repository (for dashboard visualization)."""
    return {
        "EHP": "#F97316",           # Orange
        "Portfolio": "#3B82F6",     # Blue
        "InvestorOps": "#10B981",   # Green
        "Roger-Background": "#8B5CF6",  # Purple
        "bazel-test": "#EC4899",    # Pink
        "LC": "#14B8A6",            # Teal
        "authority-frontend": "#F59E0B",  # Amber
        "ordinance-mapping": "#6366F1",   # Indigo
    }


# Content limits for indexer
MAX_ROGER_CHARS = 2000
MAX_RESPONSE_CHARS = 1000
MAX_PASTED_LINES = 10

# Polling interval for watch daemon
POLL_INTERVAL = 30  # seconds


if __name__ == "__main__":
    # Debug: print current configuration
    print(f"Platform: {platform.system()}")
    print(f"Machine: {MACHINE_NAME}")
    print(f"Is Windows: {IS_WINDOWS}")
    print(f"Is WSL: {IS_WSL}")
    print(f"Claude Projects: {CLAUDE_PROJECTS}")
    print(f"Services Dir: {SERVICES_DIR}")
    print()
    print("Repository Paths:")
    for name, path in get_repo_paths().items():
        exists = Path(path).exists()
        print(f"  {name}: {path} {'[OK]' if exists else '[NOT FOUND]'}")
    print()
    print("Claude Project Mapping:")
    for encoded, path in get_claude_project_mapping().items():
        print(f"  {encoded[:40]}... -> {path}")
