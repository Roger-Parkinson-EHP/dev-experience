#!/usr/bin/env python3
"""
Conversation Indexer V2 - Turn-Based Files

Creates individual markdown files for each conversation turn:
- New file when speaker changes (Roger → Agent or vice versa)
- Continuous blocks from same speaker append to same file
- Meaningful filenames: HHMMSS_Speaker_topic-hint.md

Output: {repo}/AI_Interaction/YYYY-MM-DD/data/
"""

import json
import os
import re
import hashlib
import socket
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import argparse

# Import from shared config
from config import (
    MACHINE_NAME,
    CLAUDE_PROJECTS,
    STATE_FILE,
    POLL_INTERVAL,
    MAX_ROGER_CHARS,
    MAX_RESPONSE_CHARS,
    MAX_PASTED_LINES,
    get_claude_project_mapping,
)

# Get repo path mapping from config
REPO_PATHS = get_claude_project_mapping()


def is_compaction_summary(text: str) -> bool:
    """Detect compaction recovery summaries."""
    markers = [
        "This session is being continued from a previous conversation",
        "conversation is summarized below",
        "Analysis:",
        "ran out of context",
    ]
    return any(marker in text[:500] for marker in markers)


def is_pasted_code(text: str) -> bool:
    """Detect if text looks like pasted code/errors."""
    lines = text.split('\n')
    if len(lines) < 5:
        return False

    code_indicators = 0
    for line in lines[:20]:
        if re.match(r'^\s*(using|import|class|def|function|public|private|//|#|{|})', line):
            code_indicators += 1
        if re.search(r'(Error|Warning|Exception|\.cs|\.py|\.js).*:\d+', line):
            code_indicators += 1

    return code_indicators > 3


STOP_WORDS = {
    'okay', 'the', 'this', 'that', 'what', 'there', 'here', 'just', 'like',
    'want', 'need', 'think', 'know', 'going', 'let', 'get', 'got', 'can',
    'will', 'would', 'could', 'should', 'have', 'has', 'had', 'been', 'being',
    'was', 'were', 'are', 'you', 'your', 'our', 'they', 'them', 'its', 'for',
    'and', 'but', 'with', 'from', 'into', 'out', 'now', 'then', 'when', 'how',
    'why', 'which', 'who', 'also', 'some', 'any', 'all', 'very', 'really',
    'actually', 'basically', 'right', 'yeah', 'yes', 'great', 'good', 'see',
    'look', 'check', 'make', 'take', 'give', 'put', 'try', 'use', 'run',
    'home', 'roger', 'projects', 'mnt', 'request', 'interrupted', 'user',
}

def extract_topic(text: str, max_words: int = 4) -> str:
    """Extract a topic hint from the first meaningful words."""
    # Skip common prefixes
    text = re.sub(r'^(okay|so|hey|hello|hi|um|uh|well|alright|anyway|,|\s)+', '', text, flags=re.I)

    # Remove file paths
    text = re.sub(r'/[\w/.-]+', '', text)

    # Get meaningful words (skip stop words)
    all_words = re.findall(r'\b[a-zA-Z]{3,}\b', text[:300])
    words = [w.lower() for w in all_words if w.lower() not in STOP_WORDS][:max_words]

    if not words:
        # Fallback to first words if all were stop words
        words = [w.lower() for w in all_words[:2]] if all_words else ["conversation"]

    topic = "-".join(words)
    # Sanitize for filename
    topic = re.sub(r'[^a-z0-9-]', '', topic)
    return topic[:40] or "conversation"


TAG_PATTERNS = {
    'error': r'\b(error|exception|failed|failure|bug|crash)\b',
    'fix': r'\b(fix|fixed|resolve|resolved|patch)\b',
    'feature': r'\b(add|added|implement|create|new feature)\b',
    'refactor': r'\b(refactor|cleanup|reorganize|restructure)\b',
    'debug': r'\b(debug|debugging|investigate|troubleshoot)\b',
    'test': r'\b(test|testing|spec|coverage)\b',
    'config': r'\b(config|configuration|settings|setup)\b',
    'ui': r'\b(ui|ux|interface|button|dialog|window|view)\b',
    'api': r'\b(api|endpoint|request|response|http)\b',
    'data': r'\b(database|db|query|sql|data|schema)\b',
}

def extract_tags(text: str) -> list:
    """Extract semantic tags from content."""
    text_lower = text.lower()
    tags = []
    for tag, pattern in TAG_PATTERNS.items():
        if re.search(pattern, text_lower):
            tags.append(tag)
    return tags[:5]  # Limit to 5 tags


def truncate_content(text: str, max_chars: int, label: str = "") -> str:
    """Truncate content with a note."""
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars].rsplit(' ', 1)[0]
    return f"{truncated}\n\n[...truncated, see JSONL for full {label}]"


def format_timestamp(ts: str) -> Tuple[str, str]:
    """Format ISO timestamp to LOCAL time (HHMMSS, HH:MM:SS)."""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        # Convert UTC to local time
        local_dt = dt.astimezone()
        return local_dt.strftime("%H%M%S"), local_dt.strftime("%H:%M:%S")
    except:
        now = datetime.now()
        return now.strftime("%H%M%S"), now.strftime("%H:%M:%S")


def classify_message(msg: Dict[str, Any]) -> str:
    """Classify message type."""
    msg_type = msg.get("type", "")
    content = msg.get("message", {}).get("content", [])

    if msg_type == "user":
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_result":
                    return "tool_output"
        return "roger"
    elif msg_type == "assistant":
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    return "agent_execution"
        return "agent_response"
    return "other"


def extract_roger_content(msg: Dict[str, Any]) -> str:
    """Extract Roger's text content."""
    content = msg.get("message", {}).get("content", "")

    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        text = "\n".join(parts)
    else:
        return ""

    # Skip compaction summaries
    if is_compaction_summary(text):
        return "[Session recovered from compaction]"

    # Truncate pasted code
    if is_pasted_code(text):
        lines = text.split('\n')
        if len(lines) > MAX_PASTED_LINES:
            preview = '\n'.join(lines[:MAX_PASTED_LINES])
            return f"{preview}\n\n[...{len(lines) - MAX_PASTED_LINES} more lines, see JSONL]"

    # Truncate very long input
    return truncate_content(text, MAX_ROGER_CHARS, "input")


def extract_agent_response(msg: Dict[str, Any]) -> str:
    """Extract agent's text response."""
    content = msg.get("message", {}).get("content", [])

    if isinstance(content, str):
        return truncate_content(content, MAX_RESPONSE_CHARS, "response")

    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            text = item.get("text", "")
            if text.strip():
                parts.append(text)

    if not parts:
        return ""

    combined = "\n".join(parts)
    return truncate_content(combined, MAX_RESPONSE_CHARS, "response")


def extract_agent_execution(msg: Dict[str, Any]) -> str:
    """Extract agent's tool calls as one-liners."""
    content = msg.get("message", {}).get("content", [])

    if not isinstance(content, list):
        return ""

    lines = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "tool_use":
            name = item.get("name", "Unknown")
            inp = item.get("input", {})

            if name == "Bash":
                cmd = inp.get("command", "")[:60]
                lines.append(f"- **Bash**: `{cmd}...`")
            elif name == "Read":
                path = Path(inp.get("file_path", "")).name
                lines.append(f"- **Read**: `{path}`")
            elif name == "Write":
                path = Path(inp.get("file_path", "")).name
                lines.append(f"- **Write**: `{path}`")
            elif name == "Edit":
                path = Path(inp.get("file_path", "")).name
                lines.append(f"- **Edit**: `{path}`")
            elif name == "Grep":
                pattern = inp.get("pattern", "")[:30]
                lines.append(f"- **Grep**: `{pattern}`")
            elif name == "Glob":
                pattern = inp.get("pattern", "")[:30]
                lines.append(f"- **Glob**: `{pattern}`")
            elif name == "Task":
                desc = inp.get("description", "subagent")[:40]
                lines.append(f"- **Task**: {desc}")
            else:
                lines.append(f"- **{name}**")

    return "\n".join(lines) if lines else ""


class TurnBasedIndexer:
    """Indexes conversations into turn-based files."""

    def __init__(self, repo_path: str, date_str: str):
        self.repo_path = Path(repo_path)
        self.date_str = date_str
        self.output_dir = self.repo_path / "AI_Interaction" / date_str / "data"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.current_speaker = None
        self.current_file = None
        self.seen_hashes = set()

    def get_content_hash(self, text: str) -> str:
        """Get hash for deduplication."""
        return hashlib.md5(text.encode()).hexdigest()[:16]

    def create_turn_file(self, timestamp: str, speaker: str, first_content: str) -> Path:
        """Create a new turn file. Returns None if content already exists."""
        ts_file, ts_display = format_timestamp(timestamp)
        topic = extract_topic(first_content)

        # Check if this content already exists (dedup)
        content_hash = self.get_content_hash(f"{timestamp}:{speaker}:{first_content}")
        if content_hash in self.seen_hashes:
            return None
        self.seen_hashes.add(content_hash)

        filename = f"{ts_file}_{speaker}_{topic}.md"
        filepath = self.output_dir / filename

        # If file exists with same name, check if content matches
        if filepath.exists():
            existing_content = filepath.read_text()
            if first_content[:100] in existing_content:
                # Same content, skip
                return None
            # Different content but same timestamp/topic - this shouldn't create dupes
            # Just use the existing file
            return None

        # Write header
        branch = ""  # Could extract from msg if needed
        header = f"# {speaker} | {self.date_str} {ts_display}\n\n"
        filepath.write_text(header)

        return filepath

    def append_to_turn(self, filepath: Path, timestamp: str, content: str, msg_type: str):
        """Append content to current turn file."""
        _, ts_display = format_timestamp(timestamp)

        with open(filepath, 'a', encoding='utf-8') as f:
            if msg_type == "roger":
                f.write(f"## ({ts_display})\n")
                for line in content.split('\n'):
                    f.write(f"> {line}\n")
                f.write("\n")
            elif msg_type == "agent_response":
                f.write(f"## ({ts_display})\n")
                f.write(f"{content}\n\n")
            elif msg_type == "agent_execution":
                f.write(f"## ({ts_display}) [tools]\n")
                f.write(f"{content}\n\n")

    def process_message(self, msg: Dict[str, Any]) -> Optional[str]:
        """Process a single message, return filename if new file created."""
        # Skip metadata
        if msg.get("_meta"):
            return None

        msg_type = classify_message(msg)

        # Skip tool outputs entirely
        if msg_type == "tool_output" or msg_type == "other":
            return None

        # Determine speaker
        speaker = "Roger" if msg_type == "roger" else "Agent"

        # Extract content based on type
        if msg_type == "roger":
            content = extract_roger_content(msg)
        elif msg_type == "agent_response":
            content = extract_agent_response(msg)
        elif msg_type == "agent_execution":
            content = extract_agent_execution(msg)
        else:
            return None

        if not content or not content.strip():
            return None

        # Deduplicate
        content_hash = self.get_content_hash(content)
        if content_hash in self.seen_hashes:
            return None
        self.seen_hashes.add(content_hash)

        timestamp = msg.get("timestamp", datetime.now().isoformat())
        new_file_created = None

        # Check if speaker changed
        if speaker != self.current_speaker:
            # New turn - create new file
            new_file = self.create_turn_file(timestamp, speaker, content)
            if new_file:  # Not a duplicate
                self.current_file = new_file
                new_file_created = self.current_file.name
            self.current_speaker = speaker

        # Append to current file
        if self.current_file:
            self.append_to_turn(self.current_file, timestamp, content, msg_type)

        return new_file_created


def generate_daily_index(output_dir: Path, date_str: str):
    """Generate a YAML index for all files in a day's folder."""
    import yaml

    md_files = sorted(output_dir.glob("*.md"))
    if not md_files:
        return

    index_data = {
        'meta': {
            'generated_at': datetime.now().isoformat(),
            'date': date_str,
            'machine': MACHINE_NAME,
            'total_files': len(md_files),
            'system': 'Conversation Indexer V2'
        },
        'turns': []
    }

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Extract headers (# lines)
            headers = []
            for line in lines:
                if line.startswith('#'):
                    header_text = line.lstrip('#').strip()
                    if header_text:
                        headers.append(header_text)

            # Parse filename: HHMMSS_Speaker_topic.md
            parts = md_file.stem.split('_', 2)
            timestamp = parts[0] if len(parts) > 0 else ""
            speaker = parts[1] if len(parts) > 1 else ""
            topic = parts[2] if len(parts) > 2 else ""

            # Get preview (first quoted line for Roger, first paragraph for Agent)
            preview = ""
            for line in lines[2:]:  # Skip header lines
                stripped = line.strip()
                if speaker == "Roger" and stripped.startswith('>'):
                    preview = stripped[1:].strip()[:150]
                    break
                elif speaker == "Agent" and stripped and not stripped.startswith('#'):
                    preview = stripped[:150]
                    break

            word_count = len(content.split())
            tags = extract_tags(content)

            turn_info = {
                'filename': md_file.name,
                'speaker': speaker,
                'timestamp': f"{timestamp[:2]}:{timestamp[2:4]}:{timestamp[4:]}" if len(timestamp) == 6 else timestamp,
                'topic': topic.replace('-', ' '),
                'headers': headers[:5],  # First 5 headers
                'preview': preview,
                'word_count': word_count,
                'token_estimate': int(word_count * 0.75),
            }
            if tags:
                turn_info['tags'] = tags
            index_data['turns'].append(turn_info)

        except Exception as e:
            print(f"  Warning: Could not index {md_file.name}: {e}")

    # Write index
    index_path = output_dir / f"{date_str}_Index.yaml"
    with open(index_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(index_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"  [Index] {index_path.name} ({len(md_files)} turns)")


def load_state() -> Dict[str, int]:
    """Load the state file tracking last processed positions."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {}


def save_state(state: Dict[str, int]):
    """Save the state file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def process_session_file(jsonl_path: Path, repo_path: str, start_pos: int = 0) -> Tuple[List[str], int]:
    """Process a JSONL session file into turn-based markdown files.

    Now handles multi-day sessions by creating separate indexers per date.
    Returns (created_files, final_position).
    """
    created_files = []
    indexers = {}  # date_str -> TurnBasedIndexer

    def get_indexer(timestamp: str) -> TurnBasedIndexer:
        """Get or create indexer for the LOCAL date of this timestamp."""
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            # Convert to local time for date folder
            local_dt = dt.astimezone()
            date_str = local_dt.strftime("%Y-%m-%d")
        except:
            date_str = datetime.now().strftime("%Y-%m-%d")

        if date_str not in indexers:
            indexers[date_str] = TurnBasedIndexer(repo_path, date_str)
        return indexers[date_str]

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        # Seek to last processed position
        if start_pos > 0:
            f.seek(start_pos)

        for line in f:
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
                ts = msg.get("timestamp", "")
                if ts:
                    indexer = get_indexer(ts)
                    new_file = indexer.process_message(msg)
                    if new_file:
                        created_files.append(new_file)
            except json.JSONDecodeError:
                continue

        final_pos = f.tell()

    return created_files, final_pos


def clean_data_folder(repo_path: str):
    """Delete existing turn files and indexes for clean regeneration."""
    ai_dir = Path(repo_path) / "AI_Interaction"
    if not ai_dir.exists():
        return 0

    deleted = 0
    for date_folder in ai_dir.iterdir():
        if date_folder.is_dir() and len(date_folder.name) == 10:  # YYYY-MM-DD
            data_subfolder = date_folder / "data"
            if data_subfolder.exists():
                for f in data_subfolder.glob("*.md"):
                    f.unlink()
                    deleted += 1
                for f in data_subfolder.glob("*.yaml"):
                    f.unlink()
                    deleted += 1
    return deleted


def main():
    parser = argparse.ArgumentParser(description="Conversation Indexer V2 - Turn-Based Files")
    parser.add_argument("--repo", "-r", action="append", help="Filter to specific repos")
    parser.add_argument("--once", action="store_true", help="Process once and exit")
    parser.add_argument("--file", "-f", help="Process specific JSONL file")
    parser.add_argument("--clean", action="store_true", help="Delete existing files before regenerating")
    parser.add_argument("--full", action="store_true", help="Full reindex (ignore saved state)")
    args = parser.parse_args()

    print("Conversation Indexer V2 - Turn-Based Files")
    print("Output: {repo}/AI_Interaction/YYYY-MM-DD/data/")
    print()

    # Load incremental state
    state = {} if args.clean or args.full else load_state()
    if state:
        print(f"Incremental mode: {len(state)} files tracked")
    else:
        print("Full index mode")

    if args.file:
        # Process specific file
        jsonl_path = Path(args.file)
        if not jsonl_path.exists():
            print(f"File not found: {jsonl_path}")
            return

        # Determine repo from path
        repo_path = None
        for encoded, path in REPO_PATHS.items():
            if encoded in str(jsonl_path.parent):
                repo_path = path
                break

        if not repo_path:
            print(f"Could not determine repo for: {jsonl_path}")
            return

        print(f"Processing: {jsonl_path.name}")
        files, _ = process_session_file(jsonl_path, repo_path, 0)
        print(f"Created {len(files)} turn files")
        for f in files[:10]:
            print(f"  - {f}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")
        return

    # Process all sessions
    processed_repos = []
    total_new_files = 0
    dates_modified = set()

    for project_dir in CLAUDE_PROJECTS.iterdir():
        if not project_dir.is_dir():
            continue

        project_name = project_dir.name
        repo_path = REPO_PATHS.get(project_name)

        if not repo_path:
            continue

        if args.repo and not any(r in project_name for r in args.repo):
            continue

        print(f"\n=== {Path(repo_path).name} ===")
        processed_repos.append(repo_path)

        # Clean existing files if requested
        if args.clean:
            deleted = clean_data_folder(repo_path)
            if deleted:
                print(f"  [Cleaned] {deleted} existing files")

        for jsonl_file in sorted(project_dir.glob("*.jsonl")):
            if "agent-" in jsonl_file.name:
                continue

            file_key = str(jsonl_file)
            file_size = jsonl_file.stat().st_size
            last_pos = state.get(file_key, 0)

            # Skip if file hasn't grown
            if last_pos >= file_size:
                continue

            if last_pos > 0:
                print(f"Processing: {jsonl_file.name} (incremental from {last_pos})")
            else:
                print(f"Processing: {jsonl_file.name}")

            files, final_pos = process_session_file(jsonl_file, repo_path, last_pos)
            state[file_key] = final_pos

            if files:
                print(f"  Created {len(files)} turn files")
                total_new_files += len(files)
                # Track which dates were modified
                for f in files:
                    # Extract date from parent folder path
                    dates_modified.add(Path(repo_path) / "AI_Interaction")

    # Save state for next incremental run
    save_state(state)
    print(f"\nState saved: {len(state)} files tracked")

    # Only regenerate indexes if we created new files OR full mode
    if total_new_files > 0 or args.full or args.clean:
        print("\n=== Generating YAML Indexes ===")
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - __import__('datetime').timedelta(days=1)).strftime("%Y-%m-%d")

        for repo_path in processed_repos:
            ai_dir = Path(repo_path) / "AI_Interaction"
            if not ai_dir.exists():
                continue

            for date_folder in sorted(ai_dir.iterdir()):
                if date_folder.is_dir() and len(date_folder.name) == 10:  # YYYY-MM-DD
                    # In incremental mode, only regenerate today and yesterday
                    if not (args.full or args.clean):
                        if date_folder.name not in (today, yesterday):
                            continue
                    data_subfolder = date_folder / "data"
                    if data_subfolder.exists():
                        generate_daily_index(data_subfolder, date_folder.name)
    else:
        print("\nNo new files created, skipping index regeneration.")

    print(f"\nDone! Created {total_new_files} new turn files.")


if __name__ == "__main__":
    main()
