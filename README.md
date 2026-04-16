# UK AI Regulation Compliance MCP Server

> **By [MEOK AI Labs](https://meok.ai)** -- Sovereign AI tools for everyone.

First-mover compliance tool for the UK's upcoming AI regulatory framework (expected mid-2026). Classify risk under the UK approach, check AISI alignment, compare EU vs UK regulation, assess organizational readiness, and generate UK-specific AI Impact Assessments.

[![MCPize](https://img.shields.io/badge/MCPize-Listed-blue)](https://mcpize.com/mcp/uk-ai-act)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-255+_servers-purple)](https://meok.ai)

## Features

- UK-specific risk classification (Unacceptable, High, Limited, Minimal)
- AI Safety Institute (AISI) alignment scoring across 8 weighted principles
- EU AI Act vs UK framework comparison across 8 regulatory dimensions
- Organizational readiness assessment with priority-ranked checklist
- AI Impact Assessment (AIA) document generation with 7 structured sections
- Automatic sector-specific regulator mapping (FCA, ICO, Ofcom, MHRA, CMA, etc.)
- Built-in rate limiting (10 free/day) and API key authentication

## Tools

| Tool | Description |
|------|-------------|
| `classify_uk_risk` | Classify AI system risk under UK framework -- detects unacceptable uses, high-risk sectors, transparency obligations |
| `check_aisi_alignment` | Check alignment with AISI standards across 8 principles: safety, transparency, accountability, fairness, privacy, security, contestability, oversight |
| `compare_eu_uk` | Compare EU AI Act vs UK approach across 8 dimensions: regulation, risk, enforcement, scope, conformity, timeline, sandboxes, GPAI |
| `assess_readiness` | Assess organizational readiness -- AI inventory, risk assessment, governance, DPIA, bias testing, transparency, incident response, training |
| `generate_impact_assessment` | Generate a UK-specific AI Impact Assessment covering system overview, data processing, rights, safety, transparency, oversight, monitoring |

## UK Regulatory Framework Coverage

### Risk Categories
| Category | Outcome | Examples |
|----------|---------|----------|
| Unacceptable | PROHIBITED | Social scoring, subliminal manipulation, mass surveillance |
| High | Requirements apply | Critical infrastructure, healthcare, employment, law enforcement |
| Limited | Transparency obligations | Chatbots, deepfakes, emotion recognition, AI-generated content |
| Minimal | Voluntary codes | Spam filters, AI games, inventory management |

### AISI Principles
| Principle | Weight |
|-----------|--------|
| Pre-deployment Safety Testing | 10 |
| Transparency and Explainability | 9 |
| Accountability Mechanisms | 9 |
| Data Protection and Privacy | 9 |
| Security and Resilience | 9 |
| Fairness and Non-Discrimination | 8 |
| Human Oversight and Control | 8 |
| Contestability and Redress | 7 |

## Quick Start

```bash
pip install mcp
git clone https://github.com/CSOAI-ORG/uk-ai-act-mcp.git
cd uk-ai-act-mcp
python server.py
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "uk-ai-act": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/uk-ai-act-mcp"
    }
  }
}
```

## Usage Examples

```python
# Classify UK risk level
result = classify_uk_risk(
    system_description="AI-powered recruitment screening tool",
    sector="employment",
    makes_autonomous_decisions=True,
    affects_individuals=True
)

# Check AISI alignment
result = check_aisi_alignment(
    system_name="RecruitAI",
    has_safety_testing=True,
    has_transparency_docs=True,
    has_fairness_testing=True,
    has_human_oversight=True
)

# Compare EU vs UK approach
result = compare_eu_uk(aspect="enforcement")

# Assess organizational readiness
result = assess_readiness(
    organization_name="TechCorp UK",
    has_ai_inventory=True,
    has_risk_assessment=True,
    has_governance_framework=True,
    sector="financial"
)
```

## Regulatory References

- UK GDPR (UK General Data Protection Regulation)
- Equality Act 2010
- Human Rights Act 1998
- AISI Safety Evaluation Framework
- ICO AI and Data Protection Guidance
- CDEI/DSIT AI Regulation White Paper (2023)

## Pricing

| Plan | Price | Requests |
|------|-------|----------|
| Free | $0/mo | 10 requests/day |
| Pro | $29/mo | Unlimited |

## Authentication

Set `MEOK_API_KEY` environment variable. Get your key at [meok.ai/api-keys](https://meok.ai/api-keys).

## Links

- [MEOK AI Labs](https://meok.ai)
- [All MCP Servers](https://meok.ai/mcp)
- [GitHub](https://github.com/CSOAI-ORG/uk-ai-act-mcp)
