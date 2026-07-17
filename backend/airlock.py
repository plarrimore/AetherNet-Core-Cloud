import re

class TelecomAirlockGuard:
    """
    Pillar 2: Programmatic telecom airlock guard.
    Stops immediate spoof attacks or high-risk telephonic injections before invoking LLMs.
    """
    def __init__(self):
        self.malicious_patterns = [
            re.compile(r"(override|prior\s+instruction|admin\s+access)", re.IGNORECASE),
            re.compile(r"(drop\s+.*table|select\s+.*from|delete\s+from)", re.IGNORECASE)
        ]

    def verify_transaction(self, transcript_text: str, routing_source: str) -> dict:
        for pattern in self.malicious_patterns:
            if pattern.search(transcript_text) or pattern.search(routing_source):
                return {
                    "is_compromised": True,
                    "reason": "ADVERSARIAL_TELEPHONY_INJECTION_DEFLECTED",
                    "action": "HARD_BLOCK"
                }

        if not re.match(r"^\+?[1-9]\d{1,14}$", routing_source):
            return {
                "is_compromised": True,
                "reason": "MALFORMED_ROUTING_SOURCE_E164_VIOLATION",
                "action": "HARD_BLOCK"
            }

        return {"is_compromised": False, "reason": "CLEARED_AIRLOCK_GATE", "action": "PROCEED"}