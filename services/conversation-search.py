#!/usr/bin/env python3
"""
Conversation Search - Search Claude JSONL conversation history

Usage:
    python conversation-search.py "search term"
    python conversation-search.py "search term" --session SESSION_ID
    python conversation-search.py "search term" --context 5
    python conversation-search.py --list-sessions

Features:
- Full-text search across all sessions or specific session
- Returns context (messages before/after match)
- Uses YAML indexes for metadata
- Supports regex patterns
"""

import json
import re
import argparse
import sys
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import CLAUDE_PROJECTS, get_claude_project_mapping

@dataclass
class SearchResult:
    session_id: str
    timestamp: str
    speaker: str  # "user" or "assistant"
    content: str
    match_preview: str
    context_before: List[str]
    context_after: List[str]


def list_sessions() -> List[Dict[str, Any]]:
    """List all available sessions with metadata."""
    sessions = []

    for project_dir in CLAUDE_PROJECTS.iterdir():
        if not project_dir.is_dir():
            continue

        for jsonl_file in project_dir.glob("*.jsonl"):
            # Skip agent transcripts
            if "agent-" in jsonl_file.name:
                continue

            session_id = jsonl_file.stem
            stat = jsonl_file.stat()

            # Count messages
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    user_count = sum(1 for l in lines if '"type":"user"' in l)
                    asst_count = sum(1 for l in lines if '"type":"assistant"' in l)
            except:
                user_count = asst_count = 0

            sessions.append({
                "session_id": session_id,
                "project": project_dir.name,
                "size_mb": round(stat.st_size / 1024 / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "user_turns": user_count,
                "assistant_turns": asst_count,
            })

    # Sort by modified date descending
    sessions.sort(key=lambda x: x["modified"], reverse=True)
    return sessions


def search_session(
    jsonl_path: Path,
    pattern: str,
    context_lines: int = 3,
    max_results: int = 20
) -> List[SearchResult]:
    """Search a single JSONL session file."""
    results = []
    messages = []

    # Load all messages
    try:
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if entry.get("type") in ("user", "assistant"):
                        # Extract text content
                        content = ""
                        msg = entry.get("message", {})
                        if isinstance(msg, dict):
                            for block in msg.get("content", []):
                                if isinstance(block, dict) and block.get("type") == "text":
                                    content += block.get("text", "")
                                elif isinstance(block, str):
                                    content += block

                        messages.append({
                            "type": entry["type"],
                            "timestamp": entry.get("timestamp", ""),
                            "content": content,
                        })
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading {jsonl_path}: {e}")
        return []

    # Search messages
    regex = re.compile(pattern, re.IGNORECASE)
    session_id = jsonl_path.stem

    for i, msg in enumerate(messages):
        if regex.search(msg["content"]):
            # Get match preview (first match with surrounding text)
            match = regex.search(msg["content"])
            if match:
                start = max(0, match.start() - 50)
                end = min(len(msg["content"]), match.end() + 100)
                preview = msg["content"][start:end]
                if start > 0:
                    preview = "..." + preview
                if end < len(msg["content"]):
                    preview = preview + "..."
            else:
                preview = msg["content"][:150] + "..."

            # Get context
            context_before = [
                f"[{messages[j]['type']}] {messages[j]['content'][:100]}..."
                for j in range(max(0, i - context_lines), i)
            ]
            context_after = [
                f"[{messages[j]['type']}] {messages[j]['content'][:100]}..."
                for j in range(i + 1, min(len(messages), i + context_lines + 1))
            ]

            results.append(SearchResult(
                session_id=session_id,
                timestamp=msg["timestamp"],
                speaker=msg["type"],
                content=msg["content"],
                match_preview=preview,
                context_before=context_before,
                context_after=context_after,
            ))

            if len(results) >= max_results:
                break

    return results


def search_all_sessions(
    pattern: str,
    session_id: Optional[str] = None,
    context_lines: int = 3,
    max_results: int = 20
) -> List[SearchResult]:
    """Search across all sessions or a specific session."""
    all_results = []

    for project_dir in CLAUDE_PROJECTS.iterdir():
        if not project_dir.is_dir():
            continue

        for jsonl_file in project_dir.glob("*.jsonl"):
            # Skip agent transcripts
            if "agent-" in jsonl_file.name:
                continue

            # Filter by session if specified
            if session_id and session_id not in jsonl_file.stem:
                continue

            results = search_session(jsonl_file, pattern, context_lines, max_results)
            all_results.extend(results)

            if len(all_results) >= max_results:
                break

        if len(all_results) >= max_results:
            break

    return all_results[:max_results]


def format_results(results: List[SearchResult], verbose: bool = False) -> str:
    """Format search results for display."""
    if not results:
        return "No results found."

    output = []
    output.append(f"Found {len(results)} result(s):\n")

    for i, r in enumerate(results, 1):
        output.append(f"--- Result {i} ---")
        output.append(f"Session: {r.session_id[:8]}...")
        output.append(f"Speaker: {r.speaker}")
        output.append(f"Time: {r.timestamp}")
        output.append(f"Preview: {r.match_preview}")

        if verbose:
            if r.context_before:
                output.append("\nContext before:")
                for ctx in r.context_before:
                    output.append(f"  {ctx}")
            if r.context_after:
                output.append("\nContext after:")
                for ctx in r.context_after:
                    output.append(f"  {ctx}")

        output.append("")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Search Claude conversation history")
    parser.add_argument("pattern", nargs="?", help="Search pattern (regex supported)")
    parser.add_argument("--session", "-s", help="Limit to specific session ID (partial match)")
    parser.add_argument("--context", "-c", type=int, default=3, help="Number of context messages (default: 3)")
    parser.add_argument("--max", "-m", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--list-sessions", "-l", action="store_true", help="List all sessions")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show full context")
    parser.add_argument("--full", "-f", action="store_true", help="Show full message content")

    args = parser.parse_args()

    if args.list_sessions:
        sessions = list_sessions()
        print(f"Found {len(sessions)} session(s):\n")
        for s in sessions:
            print(f"  {s['session_id'][:12]}... | {s['modified']} | {s['size_mb']}MB | {s['user_turns']}u/{s['assistant_turns']}a | {s['project'][:30]}")
        return

    if not args.pattern:
        parser.print_help()
        return

    print(f"Searching for: {args.pattern}")
    if args.session:
        print(f"In session: {args.session}")
    print()

    results = search_all_sessions(
        args.pattern,
        session_id=args.session,
        context_lines=args.context,
        max_results=args.max
    )

    if args.full and results:
        for i, r in enumerate(results, 1):
            print(f"=== Result {i} ({r.speaker}) ===")
            print(r.content)
            print()
    else:
        print(format_results(results, verbose=args.verbose))


if __name__ == "__main__":
    main()
