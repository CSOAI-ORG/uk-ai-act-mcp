#!/usr/bin/env python3
"""
UK AI Regulation Compliance MCP Server
========================================
By MEOK AI Labs | https://meok.ai

First-mover compliance tool for the UK's upcoming AI regulation framework
(expected mid-2026). Covers UK risk classification, AISI alignment,
EU-UK comparison, readiness assessment, and impact assessment generation.

Install: pip install mcp
Run:     python server.py
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

# ── Authentication ──────────────────────────────────────────────
sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

_MEOK_API_KEY = os.environ.get("MEOK_API_KEY", "")


def _check_auth(api_key: str = "") -> str | None:
    if _MEOK_API_KEY and api_key != _MEOK_API_KEY:
        return "Invalid API key. Get one at https://meok.ai/api-keys"
    return None


# ── Rate limiting ───────────────────────────────────────────────
FREE_DAILY_LIMIT = 10
_usage: dict[str, list[datetime]] = defaultdict(list)


def _rl(caller: str = "anonymous", tier: str = "free") -> Optional[str]:
    if tier == "pro":
        return None
    now = datetime.now()
    cutoff = now - timedelta(days=1)
    _usage[caller] = [t for t in _usage[caller] if t > cutoff]
    if len(_usage[caller]) >= FREE_DAILY_LIMIT:
        return (
            f"Free tier limit ({FREE_DAILY_LIMIT}/day). "
            "Upgrade: https://meok.ai/mcp/uk-ai-act/pro"
        )
    _usage[caller].append(now)
    return None


# ── UK AI Regulation Knowledge Base ────────────────────────────

UK_RISK_CATEGORIES = {
    "unacceptable": {
        "description": "AI systems posing unacceptable risk to safety or rights",
        "examples": ["social scoring by government", "real-time biometric identification in public (except limited exceptions)",
                     "subliminal manipulation", "exploitation of vulnerabilities"],
        "outcome": "PROHIBITED",
    },
    "high": {
        "description": "AI systems in critical sectors requiring conformity assessment",
        "sectors": ["critical_infrastructure", "education", "employment", "essential_services",
                    "law_enforcement", "immigration", "justice", "democratic_processes"],
        "requirements": ["risk_management_system", "data_governance", "technical_documentation",
                        "record_keeping", "transparency_to_users", "human_oversight",
                        "accuracy_robustness_cybersecurity"],
        "outcome": "PERMITTED_WITH_REQUIREMENTS",
    },
    "limited": {
        "description": "AI systems with specific transparency obligations",
        "examples": ["chatbots", "emotion recognition", "deepfake generation", "AI-generated content"],
        "requirements": ["transparency_notification", "content_labeling"],
        "outcome": "TRANSPARENCY_OBLIGATIONS",
    },
    "minimal": {
        "description": "AI systems with minimal or no additional regulatory requirements",
        "examples": ["spam filters", "AI-powered games", "inventory management"],
        "requirements": ["voluntary_codes_of_conduct"],
        "outcome": "MINIMAL_REQUIREMENTS",
    },
}

AISI_PRINCIPLES = {
    "safety_testing": {"name": "Pre-deployment Safety Testing", "weight": 10,
        "description": "Rigorous safety evaluation before deployment, including red-teaming"},
    "transparency": {"name": "Transparency and Explainability", "weight": 9,
        "description": "Clear documentation of capabilities, limitations, and decision-making processes"},
    "accountability": {"name": "Accountability Mechanisms", "weight": 9,
        "description": "Clear lines of responsibility and governance structures"},
    "fairness": {"name": "Fairness and Non-Discrimination", "weight": 8,
        "description": "Bias testing and mitigation across protected characteristics"},
    "privacy": {"name": "Data Protection and Privacy", "weight": 9,
        "description": "UK GDPR compliance and data minimization"},
    "security": {"name": "Security and Resilience", "weight": 9,
        "description": "Robustness against attacks and adversarial inputs"},
    "contestability": {"name": "Contestability and Redress", "weight": 7,
        "description": "Mechanisms for challenging AI decisions"},
    "human_oversight": {"name": "Human Oversight and Control", "weight": 8,
        "description": "Meaningful human control over high-impact decisions"},
}

EU_UK_DIFFERENCES = {
    "regulatory_approach": {
        "eu": "Prescriptive, rules-based (EU AI Act - Regulation 2024/1689)",
        "uk": "Principles-based, sector-specific, pro-innovation framework",
    },
    "risk_classification": {
        "eu": "Four-tier statutory classification (Unacceptable, High, Limited, Minimal)",
        "uk": "Flexible risk-based approach adapted by existing sector regulators",
    },
    "enforcement": {
        "eu": "Centralised EU AI Office + national authorities, fines up to 7% global turnover",
        "uk": "Existing regulators (FCA, Ofcom, ICO, CMA, MHRA) with cross-cutting principles",
    },
    "scope": {
        "eu": "All AI systems placed on EU market regardless of origin",
        "uk": "Focus on high-risk applications within regulated sectors",
    },
    "conformity_assessment": {
        "eu": "Mandatory conformity assessment for high-risk AI, CE marking",
        "uk": "Sector-specific approval processes, UKCA marking where applicable",
    },
    "timeline": {
        "eu": "Phased 2024-2027 (prohibitions Feb 2025, high-risk Aug 2026)",
        "uk": "Expected legislation mid-2026, implementation 2027-2028",
    },
    "sandbox": {
        "eu": "AI regulatory sandboxes required in each member state",
        "uk": "AISI-led sandbox programme, Digital Regulation Cooperation Forum",
    },
    "general_purpose_ai": {
        "eu": "Specific provisions for GPAI models (Chapter V)",
        "uk": "Foundation Model Taskforce / AISI evaluations, voluntary commitments",
    },
}


# ── FastMCP Server ──────────────────────────────────────────────

mcp = FastMCP(
    "uk-ai-act-mcp",
    instructions=(
        "UK AI Regulation Compliance MCP Server by MEOK AI Labs. "
        "First-mover tool for the UK's upcoming AI regulatory framework. "
        "Classify risk under UK approach, check AISI alignment, compare EU vs UK, "
        "assess readiness, and generate UK-specific AI impact assessments."
    ),
)


@mcp.tool()
def classify_uk_risk(
    system_description: str,
    sector: str = "",
    makes_autonomous_decisions: bool = False,
    affects_individuals: bool = False,
    uses_biometric_data: bool = False,
    is_safety_critical: bool = False,
    caller: str = "",
    api_key: str = "",
) -> str:
    """Classify an AI system's risk level under the UK regulatory framework."""
    if err := _check_auth(api_key):
        return err
    if err := _rl(caller):
        return err

    desc_lower = system_description.lower()
    sector_lower = sector.lower()

    # Check for unacceptable risk indicators
    unacceptable_keywords = ["social scoring", "subliminal manipulation", "exploitation of vulnerab",
                             "mass surveillance", "predictive policing of individuals"]
    if any(kw in desc_lower for kw in unacceptable_keywords):
        classification = "unacceptable"
    elif (is_safety_critical or uses_biometric_data or
          sector_lower in UK_RISK_CATEGORIES["high"]["sectors"] or
          any(s in desc_lower for s in ["critical infrastructure", "law enforcement", "immigration",
                                         "employment screening", "credit scoring", "healthcare diagnosis"])):
        classification = "high"
    elif (any(kw in desc_lower for kw in ["chatbot", "deepfake", "synthetic media", "emotion recognition",
                                           "content generation"]) or
          (makes_autonomous_decisions and affects_individuals)):
        classification = "limited"
    else:
        classification = "minimal"

    cat = UK_RISK_CATEGORIES[classification]
    return json.dumps({
        "system_description": system_description,
        "sector": sector or "general",
        "uk_risk_classification": classification.upper(),
        "outcome": cat["outcome"],
        "description": cat["description"],
        "requirements": cat.get("requirements", []),
        "regulatory_bodies": _get_relevant_regulators(sector_lower),
        "assessment_date": datetime.now().isoformat(),
    }, indent=2)


def _get_relevant_regulators(sector: str) -> list[str]:
    mapping = {
        "financial": ["FCA", "PRA", "Bank of England"],
        "health": ["MHRA", "CQC", "NHS Digital"],
        "telecom": ["Ofcom"],
        "education": ["Ofsted", "OfS"],
        "employment": ["EHRC", "HSE"],
        "data": ["ICO"],
        "competition": ["CMA"],
        "energy": ["Ofgem"],
        "transport": ["DfT", "CAA"],
    }
    regulators = ["ICO"]  # Always relevant for data
    for key, regs in mapping.items():
        if key in sector:
            regulators.extend(r for r in regs if r not in regulators)
    return regulators


@mcp.tool()
def check_aisi_alignment(
    system_name: str,
    has_safety_testing: bool = False,
    has_transparency_docs: bool = False,
    has_accountability: bool = False,
    has_fairness_testing: bool = False,
    has_privacy_compliance: bool = False,
    has_security_measures: bool = False,
    has_contestability: bool = False,
    has_human_oversight: bool = False,
    caller: str = "",
    api_key: str = "",
) -> str:
    """Check alignment with UK AI Safety Institute (AISI) standards."""
    if err := _check_auth(api_key):
        return err
    if err := _rl(caller):
        return err

    checks = {
        "safety_testing": has_safety_testing,
        "transparency": has_transparency_docs,
        "accountability": has_accountability,
        "fairness": has_fairness_testing,
        "privacy": has_privacy_compliance,
        "security": has_security_measures,
        "contestability": has_contestability,
        "human_oversight": has_human_oversight,
    }

    results = []
    total_weight = 0
    weighted_score = 0
    for key, met in checks.items():
        principle = AISI_PRINCIPLES[key]
        total_weight += principle["weight"]
        if met:
            weighted_score += principle["weight"]
        results.append({
            "principle": principle["name"],
            "description": principle["description"],
            "met": met,
            "weight": principle["weight"],
        })

    score = round(weighted_score / total_weight * 100, 1) if total_weight else 0

    return json.dumps({
        "system": system_name,
        "framework": "UK AI Safety Institute Principles",
        "assessment_date": datetime.now().isoformat(),
        "alignment_score": score,
        "alignment_level": "STRONG" if score >= 80 else "MODERATE" if score >= 50 else "WEAK",
        "principles_met": sum(1 for v in checks.values() if v),
        "principles_total": len(checks),
        "results": results,
    }, indent=2)


@mcp.tool()
def compare_eu_uk(
    aspect: str = "all",
    caller: str = "",
    api_key: str = "",
) -> str:
    """Compare EU AI Act vs UK regulatory approach across key dimensions."""
    if err := _check_auth(api_key):
        return err
    if err := _rl(caller):
        return err

    if aspect.lower() == "all":
        comparisons = EU_UK_DIFFERENCES
    else:
        matching = {k: v for k, v in EU_UK_DIFFERENCES.items() if aspect.lower() in k.lower()}
        if not matching:
            return json.dumps({"error": f"Aspect '{aspect}' not found. Available: {list(EU_UK_DIFFERENCES.keys())}"})
        comparisons = matching

    return json.dumps({
        "comparison": "EU AI Act vs UK AI Regulatory Framework",
        "aspects_compared": len(comparisons),
        "comparisons": comparisons,
        "key_takeaway": (
            "The EU takes a prescriptive, rules-based approach with the AI Act, "
            "while the UK favours a principles-based, pro-innovation framework "
            "that empowers existing sector regulators. Companies operating in both "
            "jurisdictions should design for EU compliance as the higher bar, "
            "then adapt for UK sector-specific requirements."
        ),
    }, indent=2)


@mcp.tool()
def assess_readiness(
    organization_name: str,
    has_ai_inventory: bool = False,
    has_risk_assessment: bool = False,
    has_governance_framework: bool = False,
    has_data_protection_impact: bool = False,
    has_bias_testing: bool = False,
    has_transparency_measures: bool = False,
    has_incident_response: bool = False,
    has_staff_training: bool = False,
    sector: str = "",
    caller: str = "",
    api_key: str = "",
) -> str:
    """Assess organizational readiness for UK AI regulation compliance."""
    if err := _check_auth(api_key):
        return err
    if err := _rl(caller):
        return err

    checks = {
        "ai_system_inventory": {"met": has_ai_inventory, "priority": "HIGH",
            "description": "Complete inventory of all AI systems in use or development"},
        "risk_assessment": {"met": has_risk_assessment, "priority": "HIGH",
            "description": "Risk classification of each AI system"},
        "governance_framework": {"met": has_governance_framework, "priority": "HIGH",
            "description": "AI governance framework with clear accountability"},
        "data_protection_impact": {"met": has_data_protection_impact, "priority": "HIGH",
            "description": "Data Protection Impact Assessment (DPIA) for AI systems processing personal data"},
        "bias_testing": {"met": has_bias_testing, "priority": "MEDIUM",
            "description": "Testing for bias across protected characteristics (Equality Act 2010)"},
        "transparency_measures": {"met": has_transparency_measures, "priority": "MEDIUM",
            "description": "Transparency measures for AI-driven decisions"},
        "incident_response": {"met": has_incident_response, "priority": "MEDIUM",
            "description": "AI incident response and reporting procedures"},
        "staff_training": {"met": has_staff_training, "priority": "MEDIUM",
            "description": "AI literacy and responsible AI training for staff"},
    }

    passed = sum(1 for c in checks.values() if c["met"])
    high_priority = {k: v for k, v in checks.items() if v["priority"] == "HIGH"}
    high_passed = sum(1 for v in high_priority.values() if v["met"])

    score = round(passed / len(checks) * 100, 1)
    if score >= 80:
        readiness = "READY"
    elif score >= 50:
        readiness = "PARTIALLY_READY"
    else:
        readiness = "NOT_READY"

    return json.dumps({
        "organization": organization_name,
        "sector": sector or "general",
        "assessment_date": datetime.now().isoformat(),
        "readiness_level": readiness,
        "readiness_score": score,
        "checks_passed": passed,
        "checks_total": len(checks),
        "high_priority_passed": f"{high_passed}/{len(high_priority)}",
        "relevant_regulators": _get_relevant_regulators(sector.lower()),
        "checks": checks,
        "next_steps": [c["description"] for c in checks.values() if not c["met"]][:5],
    }, indent=2)


@mcp.tool()
def generate_impact_assessment(
    system_name: str,
    organization_name: str,
    system_description: str,
    purpose: str,
    data_types: str = "",
    affected_groups: str = "",
    sector: str = "",
    caller: str = "",
    api_key: str = "",
) -> str:
    """Generate a UK-specific AI Impact Assessment (AIA) document."""
    if err := _check_auth(api_key):
        return err
    if err := _rl(caller):
        return err

    return json.dumps({
        "document_type": "UK AI Impact Assessment",
        "generated": datetime.now().isoformat(),
        "version": "1.0",
        "system": {
            "name": system_name,
            "organization": organization_name,
            "description": system_description,
            "purpose": purpose,
            "sector": sector or "general",
        },
        "sections": [
            {"section": "1. System Overview",
             "content": f"{system_name} is deployed by {organization_name} for the purpose of {purpose}.",
             "status": "DRAFT"},
            {"section": "2. Data Processing",
             "content": f"Data types processed: {data_types or 'Not specified'}. "
                        "Assess against UK GDPR Article 6 lawful basis and Article 9 special categories.",
             "requirements": ["Lawful basis identified", "Data minimization applied",
                            "Retention periods defined", "DPIA completed if required"]},
            {"section": "3. Rights Impact",
             "content": f"Affected groups: {affected_groups or 'Not specified'}. "
                        "Assess impact on rights under Equality Act 2010 and Human Rights Act 1998.",
             "requirements": ["Protected characteristics assessed", "Proportionality test conducted",
                            "Less intrusive alternatives considered"]},
            {"section": "4. Safety Assessment",
             "content": "Evaluate potential harms and safety risks per AISI guidelines.",
             "requirements": ["Failure modes identified", "Risk mitigations documented",
                            "Testing results recorded", "Monitoring plan in place"]},
            {"section": "5. Transparency",
             "content": "Document how users and affected parties are informed about AI use.",
             "requirements": ["AI disclosure provided", "Explanation of decisions available",
                            "Complaints mechanism established"]},
            {"section": "6. Human Oversight",
             "content": "Define human oversight mechanisms for the AI system.",
             "requirements": ["Human review of high-impact decisions", "Override capability",
                            "Escalation procedures defined"]},
            {"section": "7. Ongoing Monitoring",
             "content": "Plan for continuous monitoring of AI system performance and impact.",
             "requirements": ["Performance metrics defined", "Bias monitoring schedule",
                            "Incident reporting process", "Annual review planned"]},
        ],
        "regulatory_references": [
            "UK GDPR (UK General Data Protection Regulation)",
            "Equality Act 2010",
            "Human Rights Act 1998",
            "AISI Safety Evaluation Framework",
            "ICO AI and Data Protection Guidance",
            "CDEI/DSIT AI Regulation White Paper (2023)",
        ],
        "disclaimer": "TEMPLATE ONLY. Adapt to your specific regulatory obligations and seek legal advice.",
    }, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
