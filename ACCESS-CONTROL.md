# Access Control & Team Structure

How teams, roles, and permissions cascade across License Corporation's tech stack.

## Philosophy

1. **Teams are defined first** - in the organization, not per-tool
2. **Permissions cascade** - GitHub teams → GCP groups → AWS roles → other tools
3. **Role-based access** - what you can do is based on your role, not who you know
4. **Least privilege** - minimum access needed to do your job
5. **Auditable** - we can answer "who has access to what" at any time

---

## Teams

| Team | Purpose | GitHub Slug | GCP Group | AWS Role |
|------|---------|-------------|-----------|----------|
| **Dev** | Application developers | `dev` | `dev@licensecorporation.com` | `Developer` |
| **Lead Devs** | Senior engineers, architecture | `lead-devs` | `lead-devs@licensecorporation.com` | `LeadDeveloper` |
| **QA** | Quality assurance, testing | `qa` | `qa@licensecorporation.com` | `QA` |
| **DevOps** | Infrastructure, CI/CD | `devops` | `devops@licensecorporation.com` | `DevOps` |
| **SecOps** | Security operations | `secops` | `secops@licensecorporation.com` | `SecOps` |

---

## Roles & Capabilities

### Developer (`dev`)
| Tool | Access |
|------|--------|
| GitHub | Read/Write to assigned repos |
| GCP | `roles/aiplatform.user` (Vertex AI for Claude/Gemini) |
| AWS | Read-only where needed |
| Claude Code | Full access via Vertex AI |

### Lead Developer (`lead-devs`)
| Tool | Access |
|------|--------|
| GitHub | Read/Write to all repos, approve PRs |
| GCP | `roles/aiplatform.user` + `roles/viewer` |
| AWS | Read-only + deployment permissions |
| Claude Code | Full access via Vertex AI |

### QA (`qa`)
| Tool | Access |
|------|--------|
| GitHub | Read all repos, Write to test repos |
| GCP | `roles/aiplatform.user` (for AI-assisted testing) |
| AWS | Read-only to staging/test environments |
| Claude Code | Full access via Vertex AI |

### DevOps (`devops`)
| Tool | Access |
|------|--------|
| GitHub | Read/Write to all repos, manage Actions |
| GCP | `roles/editor` on infrastructure projects |
| AWS | Full access to infrastructure |
| Claude Code | Full access via Vertex AI |

### SecOps (`secops`)
| Tool | Access |
|------|--------|
| GitHub | Read all repos, manage security settings |
| GCP | `roles/securityReviewer` + audit access |
| AWS | Security audit access |
| Claude Code | Full access via Vertex AI |

---

## Repository Access Matrix

### Core Repos

| Repo | Dev | Lead | QA | DevOps | SecOps |
|------|-----|------|----|---------| -------|
| `dev-experience` | Read | Write | Read | Write | Read |
| `lc` | Write | Write | Read | Write | Read |
| `authority-frontend` | Write | Write | Read | Write | Read |
| `regulator-frontend` | Write | Write | Read | Write | Read |
| `backend-rest` | Write | Write | Read | Write | Read |
| `backend-graphql` | Write | Write | Read | Write | Read |
| `iac` | Read | Read | Read | Write | Write |

### Sensitive Repos

| Repo | Dev | Lead | QA | DevOps | SecOps |
|------|-----|------|----|---------| -------|
| `iac` | Read | Read | - | Write | Write |
| `iac-upwind-gcp-cm` | - | Read | - | Write | Write |

---

## GCP Project Access

| Project | Dev | Lead | QA | DevOps | SecOps |
|---------|-----|------|----|---------| -------|
| `licensecorporation-dev` | aiplatform.user | aiplatform.user | aiplatform.user | editor | viewer |
| `licensecorporation-staging` | viewer | viewer | viewer | editor | viewer |
| `licensecorporation-prod` | - | viewer | - | editor | securityReviewer |

---

## Onboarding Checklist

When a new team member joins:

### 1. Add to GitHub Team
```bash
gh api orgs/licensecorporation/teams/{team}/memberships/{username} -X PUT
```

### 2. Add to GCP Group
```bash
gcloud identity groups memberships add \
  --group-email="{team}@licensecorporation.com" \
  --member-email="{user}@licensecorporation.com"
```

### 3. Verify Vertex AI Access
```bash
# Have them run:
gcloud auth application-default login
gcloud auth application-default set-quota-project licensecorporation-dev
```

### 4. Clone dev-experience
```bash
git clone git@github.com:licensecorporation/dev-experience.git
cd dev-experience
.\setup\setup.ps1
```

### 5. Validate Setup
```bash
claude  # Should connect to Vertex AI
```

---

## Offboarding Checklist

When a team member leaves:

1. Remove from GitHub org
2. Remove from GCP groups
3. Remove from AWS roles
4. Revoke any API keys/tokens
5. Audit recent access logs

---

## Audit Commands

### Who's on which team?
```bash
gh api orgs/licensecorporation/teams/{team}/members --jq '.[].login'
```

### What repos can a team access?
```bash
gh api orgs/licensecorporation/teams/{team}/repos --jq '.[].name'
```

### Who has access to a repo?
```bash
gh api repos/licensecorporation/{repo}/collaborators --jq '.[].login'
```

---

## Future: Automated Provisioning

Goal: Single source of truth for team membership that cascades automatically.

```
teams.yaml → GitHub Teams
           → GCP Groups
           → AWS Roles
           → Slack Channels
           → Tool Access
```

This would be managed via IaC in the `iac` repository.

---

## Contact

- **Access requests**: #engineering on Slack
- **Security concerns**: secops@licensecorporation.com
- **Emergency access**: Contact DevOps lead
