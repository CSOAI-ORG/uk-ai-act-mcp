# UK AI Regulation Compliance MCP Server

> **By [MEOK AI Labs](https://meok.ai)** -- Sovereign AI tools for everyone.

First-mover compliance tool for the UK's upcoming AI regulatory framework (expected mid-2026). Classify risk, check AISI alignment, compare EU vs UK approaches, and generate UK-specific impact assessments.

[![MCPize](https://img.shields.io/badge/MCPize-Listed-blue)](https://mcpize.com/mcp/uk-ai-act)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-255+_servers-purple)](https://meok.ai)

## Tools

| Tool | Description |
|------|-------------|
| `classify_uk_risk` | Classify AI system risk under UK regulatory framework |
| `check_aisi_alignment` | Check alignment with UK AI Safety Institute standards |
| `compare_eu_uk` | Compare EU AI Act vs UK regulatory approach |
| `assess_readiness` | Assess organizational readiness for UK AI regulation |
| `generate_impact_assessment` | Generate a UK-specific AI Impact Assessment |

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
