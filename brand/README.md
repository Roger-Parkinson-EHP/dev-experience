# License Corporation Brand

Brand assets, guidelines, and resources for consistent visual identity across all products.

## Brand Properties

| Property | URL | Description |
|----------|-----|-------------|
| **License Corporation** | [licensecorporation.com](https://www.licensecorporation.com) | Parent company |
| **License Regulator** | [licenseregulator.com](https://www.licenseregulator.com) | Regulatory compliance platform |
| **License Authority** | [licenseauthority.com](https://www.licenseauthority.com) | Authority management |

## Color Palette

From licensecorporation.com:

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Orange | `#ef6820` | Accent, CTAs |
| Primary Purple | `#7839ee` | Brand accent |
| White | `#ffffff` | Backgrounds |
| Light Gray | `#f9f9fa` | Secondary backgrounds |
| Charcoal | `#1e1a1c` | Text, headers |
| Accent Green | `#26da42` | Success states |
| Accent Blue | `#4440ff` | Links, highlights |

## Typography

- **Primary**: Inter, Inter Variable, Inter Display
- **Secondary**: Clash Grotesk (weights: 400, 500, 600, 700)

## Brand Assets Storage

Public assets are stored in GCP:
```
gs://a4ee1cbc43b25bc8-public-website-prod/
```

Example: `https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/turbotenant.jpeg`

## Brand Guidelines Office Hours

- **Mondays**: 1-2 PM PST
- **Wednesdays**: 3-4 PM PST
- **Slack**: #brand-guidelines

## Using Brand in Documents

The [PDF Producer](../agentic-tools/pdf-producer/) supports branded document generation:

```bash
# Legal documents with LC styling
python markdown_to_pdf.py contract.md --style legal --toc --numbered

# Modern documents (VS Code style)
python markdown_to_pdf.py report.md --style modern
```

### Recommended Styles

| Document Type | Style | Theme |
|---------------|-------|-------|
| Legal contracts | `--style legal` | light |
| Technical docs | `--style modern` | dark |
| Client-facing | `--style modern` | light |
| Internal reports | `--style modern` | light or dark |

## Intellectual Property

**Everything created through License Corporation's development process is License Corporation intellectual capital.**

- It doesn't matter which AI assisted in creation
- If it goes through our dev process, it's ours
- The dev-experience repository ensures safe, compliant workflows
- FedRAMP infrastructure guarantees no training on our data

See [AI Policy v2](../legal/AI-POLICY-v2.md) for complete IP protection details.

## Contact

- **Brand questions**: #brand-guidelines on Slack
- **Legal questions**: legal@licensecorporation.com
