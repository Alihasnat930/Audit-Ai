from typing import Dict, Optional, Any

DEFAULT_CHATBOT_SOURCES = [
    "Transaction Analysis",
    "Fraud Detection Model",
    "Risk Scoring Algorithm",
    "Vendor Risk Register",
    "Audit Playbook",
]


def build_chatbot_prompt(question: str, context: Optional[Dict[str, Any]] = None) -> str:
    """Compose a prompt that grounds the chatbot on audit data."""
    context_block = ""
    if context:
        context_lines = []
        for key, value in context.items():
            context_lines.append(f"{key}: {value}")
        context_block = "Context:\n" + "\n".join(context_lines) + "\n\n"
    return (
        f"{context_block}"
        f"Sys Prompt: You are AuditAI's copilot. Answer succinctly, cite data-driven reasoning, "
        f"and mention fraud or risk controls when relevant.\n"
        f"User Question: {question}\n"
        "Respond with a plain language explanation, list risk findings, and cite any sources."
    )


def extract_sources(text: str) -> list:
    """Return the most relevant named sources from the answer."""
    found = []
    lower = text.lower()
    for candidate in DEFAULT_CHATBOT_SOURCES:
        if candidate.lower() in lower:
            found.append(candidate)
    return found or DEFAULT_CHATBOT_SOURCES[:2]
