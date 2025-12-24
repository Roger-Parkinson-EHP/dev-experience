#!/usr/bin/env python3
"""
Daily Summary Service

Generates an end-of-day summary of all conversations across repos.
Run at end of day when context is complete.

Usage:
  python3 ~/.claude/services/daily-summary.py [--date YYYY-MM-DD]
"""

import os
import yaml
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Import from shared config
from config import get_repo_paths

# Get repos from shared config
REPOS = get_repo_paths()

def load_yaml_index(repo_path: str, date_str: str) -> dict:
    """Load the YAML index for a repo and date."""
    index_path = Path(repo_path) / "AI_Interaction" / date_str / "data" / f"{date_str}_Index.yaml"
    if not index_path.exists():
        return None
    with open(index_path, 'r') as f:
        return yaml.safe_load(f)

def extract_roger_topics(turns: list) -> list:
    """Extract topics from Roger's turns."""
    roger_topics = []
    for turn in turns:
        if turn.get('speaker') == 'Roger':
            roger_topics.append({
                'time': turn.get('timestamp', ''),
                'topic': turn.get('topic', ''),
                'preview': turn.get('preview', '')[:100],
                'tags': turn.get('tags', [])
            })
    return roger_topics

def generate_summary(date_str: str) -> dict:
    """Generate summary for all repos."""
    summary = {
        'date': date_str,
        'generated_at': datetime.now().isoformat(),
        'repos': {},
        'totals': {
            'total_turns': 0,
            'roger_turns': 0,
            'agent_turns': 0,
            'total_tokens': 0,
        },
        'roger_highlights': [],
        'all_tags': defaultdict(int),
    }

    for repo_name, repo_path in REPOS.items():
        index = load_yaml_index(repo_path, date_str)
        if not index:
            summary['repos'][repo_name] = {'status': 'no_index'}
            continue

        turns = index.get('turns', [])
        roger_turns = [t for t in turns if t.get('speaker') == 'Roger']
        agent_turns = [t for t in turns if t.get('speaker') == 'Agent']

        total_tokens = sum(t.get('token_estimate', 0) for t in turns)
        roger_tokens = sum(t.get('token_estimate', 0) for t in roger_turns)

        # Collect tags
        for turn in turns:
            for tag in turn.get('tags', []):
                summary['all_tags'][tag] += 1

        # Extract Roger's topics
        roger_topics = extract_roger_topics(turns)
        summary['roger_highlights'].extend([
            {'repo': repo_name, **t} for t in roger_topics[:5]  # Top 5 per repo
        ])

        summary['repos'][repo_name] = {
            'total_turns': len(turns),
            'roger_turns': len(roger_turns),
            'agent_turns': len(agent_turns),
            'total_tokens': total_tokens,
            'roger_tokens': roger_tokens,
            'top_topics': list(set(t.get('topic', '') for t in turns[:10])),
        }

        summary['totals']['total_turns'] += len(turns)
        summary['totals']['roger_turns'] += len(roger_turns)
        summary['totals']['agent_turns'] += len(agent_turns)
        summary['totals']['total_tokens'] += total_tokens

    summary['all_tags'] = dict(summary['all_tags'])
    return summary

def print_summary(summary: dict):
    """Print human-readable summary."""
    print(f"\n{'='*60}")
    print(f"DAILY SUMMARY: {summary['date']}")
    print(f"{'='*60}\n")

    # Totals
    t = summary['totals']
    print(f"TOTALS:")
    print(f"  Total turns:  {t['total_turns']}")
    print(f"  Roger turns:  {t['roger_turns']} ({t['roger_turns']/max(t['total_turns'],1)*100:.0f}%)")
    print(f"  Agent turns:  {t['agent_turns']}")
    print(f"  Total tokens: ~{t['total_tokens']:,}")
    print()

    # Per repo
    print("BY REPO:")
    for repo, data in summary['repos'].items():
        if data.get('status') == 'no_index':
            print(f"  {repo}: No index")
        else:
            print(f"  {repo}:")
            print(f"    Turns: {data['total_turns']} ({data['roger_turns']} Roger, {data['agent_turns']} Agent)")
            print(f"    Tokens: ~{data['total_tokens']:,} ({data['roger_tokens']:,} Roger)")
    print()

    # Top tags
    if summary['all_tags']:
        print("TOP TAGS:")
        sorted_tags = sorted(summary['all_tags'].items(), key=lambda x: -x[1])[:10]
        for tag, count in sorted_tags:
            print(f"  {tag}: {count}")
    print()

    # Roger highlights
    print("ROGER'S KEY TOPICS:")
    for h in summary['roger_highlights'][:15]:
        print(f"  [{h['repo']}] {h['time']} - {h['topic']}")

    print(f"\n{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(description="Daily Summary Service")
    parser.add_argument("--date", "-d", help="Date to summarize (YYYY-MM-DD), default: yesterday")
    parser.add_argument("--today", action="store_true", help="Summarize today instead of yesterday")
    parser.add_argument("--yaml", action="store_true", help="Output as YAML")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    elif args.today:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    summary = generate_summary(date_str)

    if args.yaml:
        print(yaml.safe_dump(summary, default_flow_style=False, sort_keys=False))
    else:
        print_summary(summary)

    # Save summary to EACH repo's data folder (part of the day's index)
    for repo_name, repo_path in REPOS.items():
        repo_data_dir = Path(repo_path) / "AI_Interaction" / date_str / "data"
        if repo_data_dir.exists():
            summary_path = repo_data_dir / f"{date_str}_EOD_Summary.yaml"
            with open(summary_path, 'w') as f:
                yaml.safe_dump(summary, f, default_flow_style=False, sort_keys=False)
            print(f"Saved: {summary_path}")

    # Also save master copy to Roger-Background
    master_dir = Path(REPOS["Roger-Background"]) / "AI_Interaction" / date_str / "data"
    master_dir.mkdir(parents=True, exist_ok=True)
    master_path = master_dir / f"{date_str}_EOD_Summary.yaml"
    with open(master_path, 'w') as f:
        yaml.safe_dump(summary, f, default_flow_style=False, sort_keys=False)
    print(f"Master summary: {master_path}")

if __name__ == "__main__":
    main()
