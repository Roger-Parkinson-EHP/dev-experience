---
name: post-compact
description: Recover context after a compaction event. Use this IMMEDIATELY after seeing a compaction summary or when the conversation starts with a summary from a previous session. Do not respond to the user until you have recovered full context.
---

# Post-Compaction Context Recovery

## When to Use This Skill

Use this skill when you see ANY of these signals:
- "This session is being continued from a previous conversation"
- A compaction summary at the start of the conversation
- User mentions "we were just working on..." after a gap
- You notice the context feels thin or you're missing details

## Instructions

**STOP before responding to the user.** First recover context:

1. **Search recent history** for the current session:
```bash
cd ~/.claude/services
python conversation-search.py --list-sessions | head -5
```

2. **Get recent context** from today's work:
```bash
python conversation-search.py "INSERT_TOPIC_FROM_SUMMARY" --max 5 --verbose
```

3. **Look for specific items** mentioned in the summary:
   - Active tasks or todos
   - Files being edited
   - Errors being debugged
   - Decisions that were made

4. **Search for the last few exchanges** before compaction:
```bash
python conversation-search.py "." --session CURRENT_SESSION_ID --max 10 --full
```

## What to Recover

- **Current task**: What were we actively working on?
- **Recent changes**: What files were modified?
- **Open issues**: What problems remained unsolved?
- **User preferences**: Any specific ways the user wanted things done?
- **Context that was lost**: Details the summary might have missed

## After Recovery

Once you have context:
1. Briefly confirm what you understand about the current state
2. Ask if the user wants to continue where we left off
3. Resume work with full context

## Example

After seeing a compaction summary mentioning "statusline configuration":

```bash
python conversation-search.py "statusline" --max 3 --full
```

This recovers the actual implementation details, not just that it was mentioned.
