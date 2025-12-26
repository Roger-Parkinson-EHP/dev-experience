# Contributing to dev-experience

How to contribute to License Corporation's developer experience repository.

## Quick Start

```bash
# 1. Clone
git clone git@github.com:licensecorporation/dev-experience.git
cd dev-experience

# 2. Create a branch
git checkout -b feature/your-feature-name

# 3. Make changes

# 4. Commit
git add -A
git commit -m "Description of changes"

# 5. Push and create PR
git push origin feature/your-feature-name
# Then open PR on GitHub
```

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `production` | Stable, protected. All changes via PR. |
| `dev` | Integration branch for testing changes |
| `feature/*` | New features |
| `fix/*` | Bug fixes |

## Pull Request Process

1. **Create a branch** from `production` or `dev`
2. **Make your changes** with clear commits
3. **Push your branch** to origin
4. **Open a PR** with description of changes
5. **Get approval** from CODEOWNERS
6. **Merge** after approval

## What Belongs Here

| Content | Belongs in dev-experience |
|---------|---------------------------|
| AI tools (Claude Code, Gemini CLI) | ✅ Yes |
| Speech-to-text (WhisperFlow) | ✅ Yes |
| PDF producer | ✅ Yes |
| Brand guidelines | ✅ Yes |
| FedRAMP/Vertex AI setup | ✅ Yes |
| Access control policies | ✅ Yes |
| Onboarding docs | ✅ Yes |
| Legal/AI policies | ✅ Yes |
| Application code | ❌ No → goes to `lc` repo |
| Infrastructure code | ❌ No → goes to `iac` repo |
| Product features | ❌ No → goes to product repos |

## What Belongs in LC Repo

The [lc repository](https://github.com/licensecorporation/lc) is for:

- Application code (monorepo)
- Bazel build configuration
- Testing frameworks
- CI/CD pipelines
- Dev → Staging → Production deployment
- Integration of legacy codebases

## Code Owners

Changes to specific areas require approval from designated owners. See [CODEOWNERS](.github/CODEOWNERS) for details.

Currently all changes require approval from @Roger-Parkinson-EHP during the iteration phase.

## Commit Messages

Use clear, descriptive commit messages:

```
Add speech-to-text hotkey configuration

- Added ctrl+shift+space as default hotkey
- Updated README with usage instructions
```

## Testing Changes

Before submitting a PR:

1. **Setup scripts**: Test on fresh environment if possible
2. **Documentation**: Ensure links work, paths are correct
3. **Tools**: Verify tools still function after changes

## Getting Help

- **Questions**: #engineering on Slack
- **Issues**: Open an issue in this repo
- **Security concerns**: secops@licensecorporation.com

## AI-Assisted Contributions

You're encouraged to use Claude Code for contributions. All work created through our FedRAMP infrastructure is License Corporation intellectual capital.

```bash
# Start Claude Code
claude

# Ask it to help
"Help me add a new tool to the agentic-tools folder"
"Review this documentation for clarity"
"Create tests for this setup script"
```

See [ONBOARDING.md](ONBOARDING.md) for full setup instructions.
