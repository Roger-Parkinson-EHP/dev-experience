# License Corporation Brand

Brand assets, guidelines, and resources for consistent visual identity across all products.

## Brand Properties

| Property | URL | Description |
|----------|-----|-------------|
| **License Corporation** | [licensecorporation.com](https://www.licensecorporation.com) | Parent company |
| **License Regulator** | [licenseregulator.com](https://www.licenseregulator.com) | Regulatory compliance platform |
| **License Authority** | [licenseauthority.com](https://www.licenseauthority.com) | Authority management |

## Logo Assets (GCP Bucket)

All logos stored in: `gs://a4ee1cbc43b25bc8-public-website-prod/`

### License Corporation Logos

| Asset | URL |
|-------|-----|
| **LC Logo (Black)** | [LC_Logo_Black.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/LC_Logo_Black.png) |
| **License Authority** | [License_Authority_Logo_White_Background.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/License_Authority_Logo_White_Background.png) |

### Partner/Client Logos

| Asset | URL |
|-------|-----|
| TurboTenant | [turbotenant.jpeg](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/turbotenant.jpeg) |
| Greystar | [lg-674583fc49ae9-Greystar-Photoroom.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/lg-674583fc49ae9-Greystar-Photoroom.png) |
| US Bank | [US_BANK.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/US_BANK.png) |
| Rippling | [Rippling.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/Rippling.png) |
| Money2020 | [money2020.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/money2020.png) |
| Flint | [Logo_Flint_White.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/Logo_Flint_White.png) |
| Krypt | [Krypt_Logo-05.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/Krypt_Logo-05.png) |
| WBD | [wbd_logo.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/wbd_logo.png) |
| DLA | [DLAEmblemWebsiteHeader.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/DLAEmblemWebsiteHeader.png) |
| Cage | [cage.png](https://storage.googleapis.com/a4ee1cbc43b25bc8-public-website-prod/cage.png) |

## Color Palette

From licensecorporation.com:

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Primary Orange** | `#ef6820` | `--lc-orange` | Accent, CTAs, brand highlight |
| **Primary Purple** | `#7839ee` | `--lc-purple` | Brand accent |
| **Charcoal** | `#1e1a1c` | `--lc-charcoal` | Text, headers |
| **White** | `#ffffff` | `--lc-white` | Backgrounds |
| **Light Gray** | `#f9f9fa` | `--lc-light-gray` | Secondary backgrounds |
| **Accent Green** | `#26da42` | `--lc-green` | Success states |
| **Accent Blue** | `#4440ff` | `--lc-blue` | Links, highlights |

## Typography

| Font | Weights | Usage |
|------|---------|-------|
| **Inter** | 400, 500, 600, 700 | Primary UI font |
| **Inter Display** | 600, 700 | Headlines |
| **Clash Grotesk** | 400, 500, 600, 700 | Secondary/accent |

## Brand Guidelines Office Hours

| Day | Time (PST) |
|-----|------------|
| Monday | 1:00 - 2:00 PM |
| Wednesday | 3:00 - 4:00 PM |

**Slack**: #brand-guidelines

## Branded PDF Generation

The [PDF Producer](../agentic-tools/pdf-producer/) generates official LC-branded documents:

```bash
# Official branded document
python markdown_to_pdf.py proposal.md --branded --style legal --toc

# What --branded adds:
# - LC logo in header
# - Document title in header
# - "License Corporation - Confidential" in footer
# - Page numbers (Page X of Y)
# - Generation date
# - Orange accent border
```

### Document Types

| Document | Command |
|----------|---------|
| **Legal/Contract** | `--branded --style legal --toc --numbered` |
| **Proposal** | `--branded --style legal --toc` |
| **Internal Report** | `--branded --style modern` |
| **Public Document** | `--branded --no-confidential` |

## Intellectual Property

**Everything created through License Corporation's development process is License Corporation intellectual capital.**

- It doesn't matter which AI assisted in creation
- If it goes through our dev process, it's ours
- The dev-experience repository ensures safe, compliant workflows
- FedRAMP infrastructure guarantees no training on our data

See [AI Policy v2](../legal/AI-POLICY-v2.md) for complete IP protection details.

## Contact

- **Brand questions**: #brand-guidelines on Slack
- **Logo requests**: Upload to GCP bucket via `gsutil cp`
- **Legal questions**: legal@licensecorporation.com
