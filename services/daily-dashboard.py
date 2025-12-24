#!/usr/bin/env python3
"""
Daily Dashboard Generator

Creates a visual PNG dashboard summarizing the day's AI interactions.
Shows: turns by repo, top tags, activity timeline, git commits, key topics.

Usage:
  python3 ~/.claude/services/daily-dashboard.py [--date YYYY-MM-DD] [--today]
"""

import os
import yaml
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter

# Import from shared config
from config import get_repo_paths, get_repo_colors

# Try to import visualization libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not installed. Install with: pip install matplotlib")

# Get repos and colors from shared config
REPOS = get_repo_paths()
REPO_COLORS = get_repo_colors()

def load_yaml_index(repo_path: str, date_str: str) -> dict:
    """Load the YAML index for a repo and date."""
    index_path = Path(repo_path) / "AI_Interaction" / "data" / date_str / f"{date_str}_Index.yaml"
    if not index_path.exists():
        return None
    with open(index_path, 'r') as f:
        return yaml.safe_load(f)

def get_git_commits(repo_path: str, date_str: str) -> list:
    """Get git commits for the date."""
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--oneline", f"--since={date_str} 00:00", f"--until={date_str} 23:59", "--format=%h %s"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return [line for line in result.stdout.strip().split('\n') if line]
        return []
    except:
        return []

def parse_timestamp(ts: str) -> int:
    """Convert HH:MM:SS to minutes from midnight."""
    try:
        parts = ts.split(':')
        return int(parts[0]) * 60 + int(parts[1])
    except:
        return 0

def collect_data(date_str: str) -> dict:
    """Collect all data for the dashboard."""
    data = {
        'date': date_str,
        'repos': {},
        'all_tags': Counter(),
        'timeline': defaultdict(lambda: defaultdict(int)),  # hour -> repo -> count
        'roger_topics': [],
        'commits': {},
        'totals': {'turns': 0, 'roger': 0, 'tokens': 0}
    }

    for repo_name, repo_path in REPOS.items():
        index = load_yaml_index(repo_path, date_str)
        commits = get_git_commits(repo_path, date_str)

        data['commits'][repo_name] = commits

        if not index:
            data['repos'][repo_name] = {'turns': 0, 'roger': 0, 'tokens': 0}
            continue

        turns = index.get('turns', [])
        roger_turns = [t for t in turns if t.get('speaker') == 'Roger']

        total_tokens = sum(t.get('token_estimate', 0) for t in turns)

        data['repos'][repo_name] = {
            'turns': len(turns),
            'roger': len(roger_turns),
            'tokens': total_tokens
        }

        data['totals']['turns'] += len(turns)
        data['totals']['roger'] += len(roger_turns)
        data['totals']['tokens'] += total_tokens

        # Collect tags
        for turn in turns:
            for tag in turn.get('tags', []):
                data['all_tags'][tag] += 1

        # Timeline (by hour)
        for turn in turns:
            ts = turn.get('timestamp', '00:00:00')
            try:
                hour = int(ts.split(':')[0])
                data['timeline'][hour][repo_name] += 1
            except:
                pass

        # Roger's topics
        for turn in roger_turns[:3]:
            data['roger_topics'].append({
                'repo': repo_name,
                'time': turn.get('timestamp', ''),
                'topic': turn.get('topic', '')[:30]
            })

    return data

def generate_dashboard(data: dict, output_path: Path):
    """Generate the visual dashboard."""
    if not HAS_MATPLOTLIB:
        print("Cannot generate dashboard without matplotlib")
        return False

    fig = plt.figure(figsize=(16, 10), facecolor='#1a1a2e')
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

    # Title
    fig.suptitle(f"Daily AI Dashboard: {data['date']}",
                 fontsize=20, fontweight='bold', color='white', y=0.98)

    # 1. Turns by Repo (bar chart) - top left
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#16213e')
    repos = list(data['repos'].keys())
    turns = [data['repos'][r]['turns'] for r in repos]
    colors = [REPO_COLORS.get(r, '#888') for r in repos]
    bars = ax1.bar(repos, turns, color=colors, edgecolor='white', linewidth=0.5)
    ax1.set_ylabel('Turns', color='white')
    ax1.set_title('Turns by Repo', color='white', fontweight='bold')
    ax1.tick_params(colors='white')
    for spine in ax1.spines.values():
        spine.set_color('#333')
    # Add value labels
    for bar, val in zip(bars, turns):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                str(val), ha='center', va='bottom', color='white', fontsize=9)

    # 2. Roger vs Agent split (pie) - top middle
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#1a1a2e')
    roger = data['totals']['roger']
    agent = data['totals']['turns'] - roger
    if roger + agent > 0:
        ax2.pie([roger, agent], labels=['Roger', 'Agent'],
                colors=['#F97316', '#3B82F6'], autopct='%1.0f%%',
                textprops={'color': 'white'}, wedgeprops={'edgecolor': '#1a1a2e'})
    ax2.set_title('Roger vs Agent Turns', color='white', fontweight='bold')

    # 3. Top Tags (horizontal bar) - top right
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor('#16213e')
    top_tags = data['all_tags'].most_common(8)
    if top_tags:
        tags, counts = zip(*top_tags)
        y_pos = range(len(tags))
        ax3.barh(y_pos, counts, color='#10B981', edgecolor='white', linewidth=0.5)
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(tags, color='white')
        ax3.invert_yaxis()
    ax3.set_title('Top Tags', color='white', fontweight='bold')
    ax3.tick_params(colors='white')
    for spine in ax3.spines.values():
        spine.set_color('#333')

    # 4. Activity Timeline (stacked area) - middle row, full width
    ax4 = fig.add_subplot(gs[1, :])
    ax4.set_facecolor('#16213e')
    hours = list(range(24))
    bottom = [0] * 24
    for repo in repos:
        values = [data['timeline'].get(h, {}).get(repo, 0) for h in hours]
        ax4.fill_between(hours, bottom, [b + v for b, v in zip(bottom, values)],
                        label=repo, color=REPO_COLORS.get(repo, '#888'), alpha=0.7)
        bottom = [b + v for b, v in zip(bottom, values)]
    ax4.set_xlim(0, 23)
    ax4.set_xlabel('Hour of Day', color='white')
    ax4.set_ylabel('Turns', color='white')
    ax4.set_title('Activity Timeline', color='white', fontweight='bold')
    ax4.legend(loc='upper right', facecolor='#16213e', edgecolor='#333',
               labelcolor='white', fontsize=8)
    ax4.tick_params(colors='white')
    for spine in ax4.spines.values():
        spine.set_color('#333')

    # 5. Summary Stats (text) - bottom left
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.set_facecolor('#16213e')
    ax5.axis('off')
    stats_text = f"""
TOTALS
──────────────
Turns: {data['totals']['turns']:,}
Roger: {data['totals']['roger']:,}
Tokens: ~{data['totals']['tokens']:,}

TOP REPOS
──────────────
"""
    for repo in sorted(data['repos'].keys(), key=lambda r: -data['repos'][r]['turns']):
        stats_text += f"{repo}: {data['repos'][repo]['turns']}\n"

    ax5.text(0.1, 0.9, stats_text, transform=ax5.transAxes, fontsize=10,
            color='white', verticalalignment='top', fontfamily='monospace')

    # 6. Git Commits (text) - bottom middle
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.set_facecolor('#16213e')
    ax6.axis('off')
    commits_text = "GIT COMMITS\n──────────────\n"
    total_commits = 0
    for repo, commits in data['commits'].items():
        if commits:
            commits_text += f"\n{repo} ({len(commits)}):\n"
            for c in commits[:3]:
                commits_text += f"  • {c[:40]}\n"
            total_commits += len(commits)
    if total_commits == 0:
        commits_text += "(no commits today)"
    ax6.text(0.1, 0.9, commits_text, transform=ax6.transAxes, fontsize=9,
            color='white', verticalalignment='top', fontfamily='monospace')

    # 7. Roger's Topics (text) - bottom right
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.set_facecolor('#16213e')
    ax7.axis('off')
    topics_text = "ROGER'S TOPICS\n──────────────\n"
    for t in data['roger_topics'][:8]:
        topics_text += f"\n[{t['repo'][:3]}] {t['time']}\n  {t['topic']}\n"
    ax7.text(0.1, 0.9, topics_text, transform=ax7.transAxes, fontsize=9,
            color='white', verticalalignment='top', fontfamily='monospace')

    # Save
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='#1a1a2e', edgecolor='none')
    plt.close()
    return True

def main():
    parser = argparse.ArgumentParser(description="Daily Dashboard Generator")
    parser.add_argument("--date", "-d", help="Date (YYYY-MM-DD), default: yesterday")
    parser.add_argument("--today", action="store_true", help="Generate for today")
    parser.add_argument("--output", "-o", help="Output path for PNG")
    args = parser.parse_args()

    if args.date:
        date_str = args.date
    elif args.today:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Generating dashboard for {date_str}...")

    data = collect_data(date_str)

    # Output path - save to EACH repo's data folder
    if args.output:
        output_path = Path(args.output)
        if generate_dashboard(data, output_path):
            print(f"Dashboard saved: {output_path}")
    else:
        # Save to each repo's data folder
        for repo_name, repo_path in REPOS.items():
            repo_data_dir = Path(repo_path) / "AI_Interaction" / "data" / date_str
            if repo_data_dir.exists():
                output_path = repo_data_dir / f"{date_str}_Dashboard.png"
                if generate_dashboard(data, output_path):
                    print(f"Dashboard saved: {output_path}")

        # Also save master copy to Roger-Background
        master_dir = Path(REPOS["Roger-Background"]) / "AI_Interaction" / "data" / date_str
        master_dir.mkdir(parents=True, exist_ok=True)
        master_path = master_dir / f"{date_str}_Dashboard.png"
        if generate_dashboard(data, master_path):
            print(f"Master dashboard: {master_path}")

if __name__ == "__main__":
    main()
