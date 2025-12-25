# License Corporation AI Development Policy

**Version:** 2.0
**Effective Date:** December 2025
**Supersedes:** AI Policy v1.0 (August 14, 2025)

---

## 1. Purpose

This policy establishes the framework for AI-assisted software development at License Corporation. It replaces the restrictive controls of v1.0 with a **compliance-by-design** approach that enables productive AI usage within a secure, auditable environment.

The key principle: **Rather than restricting AI usage, we provide compliant tools and infrastructure that make it impossible to violate policy within the approved environment.**

---

## 2. Scope

This policy applies to all Personnel (employees, contractors, consultants) who:
- Write, review, or maintain code for License Corporation
- Use AI tools for development purposes
- Access company repositories or development environments

---

## 3. Compliance Framework

### 3.1 Authoritative Source

The **[dev-experience repository](https://github.com/licensecorporation/dev-experience)** is the authoritative source for:
- Approved AI tools and models
- Configuration standards
- Usage patterns and best practices
- Compliance validation scripts

Personnel must use tools and configurations as documented in this repository. Updates to approved tools require approval from designated Code Owners.

### 3.2 FedRAMP Compliance

All AI inference MUST occur through FedRAMP-authorized infrastructure:

| Provider | Service | Authorization | Data Training |
|----------|---------|---------------|---------------|
| Google Cloud | Vertex AI Model Garden | FedRAMP High (us-east5) | **None** |
| AWS | Bedrock GovCloud | FedRAMP High | **None** |
| Microsoft | Azure Government | FedRAMP High | **None** |

**Current Implementation:** Google Cloud Vertex AI in `us-east5` region.

### 3.3 Data Protection Guarantees

When using approved infrastructure:
- Data is **NOT used for model training**
- Data remains within **US FedRAMP boundary**
- All API calls are **logged in Cloud Logging** for audit
- Data residency: **United States only**

---

## 4. Approved Tools

### 4.1 Primary Development Tool

| Tool | Model | Infrastructure | Status |
|------|-------|----------------|--------|
| **Claude Code** | Claude Opus 4.5, Sonnet 4.5 | GCP Vertex AI (us-east5) | **Approved** |

Claude Code is approved for full AI-assisted development including:
- Code generation and refactoring
- Architecture design
- Debugging and troubleshooting
- Documentation
- Repository-wide analysis

### 4.2 Additional Models (via MCP)

| Model | Provider | Region | Compliance |
|-------|----------|--------|------------|
| Gemini 2.5 Pro | Google | us-east5 | FedRAMP High |
| Gemini 2.5 Flash | Google | us-east5 | FedRAMP High |
| Gemini 3 Pro Preview | Google | global | IP-safe (no training) |
| Gemini 3 Flash Preview | Google | global | IP-safe (no training) |

### 4.3 Prohibited Tools

Tools that send data outside FedRAMP boundaries remain prohibited:
- Browser-based AI (ChatGPT web, Gemini web, Perplexity) for code tasks
- Windsurf, Trae, and similar tools without FedRAMP authorization
- Any tool not configured per dev-experience specifications

---

## 5. Development Standards

### 5.1 Safe Field of Play

The dev-experience repository defines a "safe field of play" where:
- All approved tools are pre-configured for compliance
- Validation scripts verify correct setup
- Developers have freedom within compliant boundaries

### 5.2 Orchestration Controls

The **[lc repository](https://github.com/licensecorporation/lc)** (product codebase) implements:
- Automated testing via CI/CD
- Code owner approval requirements
- Pre-commit hooks and linting
- Security scanning

### 5.3 Code Ownership

Changes to compliance-critical files require approval from designated Code Owners:
- AI policy documents
- Tool configurations
- Security-related code
- Infrastructure definitions

---

## 6. Responsibilities

### 6.1 Personnel

- Use only tools documented in dev-experience repo
- Run validation scripts before starting work
- Report any compliance concerns to security team
- Keep local environment configured per specifications

### 6.2 Code Owners

- Review and approve changes to policy documents
- Evaluate new tools for compliance
- Maintain dev-experience repository
- Conduct periodic audits

### 6.3 Platform Team

- Maintain GCP/Vertex AI infrastructure
- Monitor Cloud Logging for anomalies
- Manage IAM and access controls
- Update validation scripts

---

## 7. Setup and Validation

### 7.1 Initial Setup (One-Time)

Personnel must run the setup script to provision their Claude Code environment:

```bash
# Clone the repository
git clone https://github.com/licensecorporation/dev-experience
cd dev-experience

# Windows (PowerShell as Admin or Developer Mode enabled)
.\setup.ps1

# macOS/Linux
chmod +x setup.sh && ./setup.sh
```

This creates symlinks from `~/.claude/` to the dev-experience repository, ensuring:
- **Skills** are automatically available
- **MCP servers** for Gemini are configured
- **Updates apply instantly** via `git pull`
- **No Claude/Anthropic attribution** on commits or PRs

### 7.2 Validation

After setup, validate the configuration:

```bash
# Windows
.\claude-code\vertex-ai-model-garden\windows\validate-vertex-setup.ps1

# macOS/Linux
./claude-code/vertex-ai-model-garden/unix/validate-vertex-setup.sh
```

Expected result: All checks pass, confirming FedRAMP-compliant configuration.

---

## 8. Audit and Monitoring

### 8.1 Cloud Logging

All AI API calls are logged in GCP Cloud Logging:
- Timestamp
- User identity
- Model used
- Region
- Request/response metadata

### 8.2 Periodic Review

Code Owners will conduct quarterly reviews of:
- Tool usage patterns
- New tools for evaluation
- Policy effectiveness
- Compliance incidents

---

## 9. Changes from v1.0

| v1.0 Restriction | v2.0 Approach |
|-----------------|---------------|
| 50% AI limit per task | No limit when using compliant tools |
| Prohibited: inputting code to AI | Allowed: Vertex AI doesn't train on data |
| Limited approved tools | Full Claude Code + Gemini via Vertex AI |
| "Vibe Coding" prohibited | Allowed within compliant environment |
| Manual compliance checking | Automated validation scripts |

---

## 10. Amendments

This policy is maintained in the dev-experience repository. Changes require:
1. Pull request with justification
2. Code Owner approval
3. Security review for material changes
4. Version increment and changelog

---

## 11. Acknowledgment

By using License Corporation development tools and repositories, Personnel acknowledge:
- They have read and understand this policy
- They will use only approved tools and configurations
- They will report compliance concerns promptly
- Violations may result in disciplinary action

**This policy supersedes AI Policy v1.0 dated August 14, 2025.**

---

## References

- [dev-experience repository](https://github.com/licensecorporation/dev-experience)
- [Vertex AI FedRAMP Authorization](https://cloud.google.com/security/compliance/fedramp)
- [Anthropic Claude FedRAMP](https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high)
- [GCP us-east5 Compliance](https://cloud.google.com/about/locations#americas)
