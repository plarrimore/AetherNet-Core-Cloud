import psycopg
from psycopg.rows import dict_row

class SubscriberRegistryMemoryStore:
    """
    Pillar 5: Persistent subscriber historical registry.
    Retains long-term baseline trust statuses across call sessions.
    """
    def __init__(self, db_url: str):
        self.db_url = db_url
        self._init_tables()

    def _init_tables(self):
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS subscriber_trust_registry (
                        phone_number VARCHAR(50) PRIMARY KEY,
                        subscriber_tier VARCHAR(50) DEFAULT 'STANDARD',
                        historical_fraud_reports INT DEFAULT 0,
                        is_trusted BOOLEAN DEFAULT TRUE
                    );
                """)
                # Seed baseline data
                cur.execute("""
                    INSERT INTO subscriber_trust_registry (phone_number, subscriber_tier, historical_fraud_reports, is_trusted)
                    VALUES 
                        ('+15550199', 'VIP_ENTERPRISE', 0, TRUE),
                        ('+15550188', 'BASIC_RETAIL', 12, FALSE)
                    ON CONFLICT (phone_number) DO NOTHING;
                """)
                conn.commit()

    def fetch_subscriber_profile(self, phone: str) -> dict:
        try:
            with psycopg.connect(self.db_url, row_factory=dict_row) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM subscriber_trust_registry WHERE phone_number = %s;", (phone,))
                    row = cur.fetchone()
                    return row if row else {
                        "phone_number": phone,
                        "subscriber_tier": "GUEST_ROUTING",
                        "historical_fraud_reports": 0,
                        "is_trusted": True
                    }
        except Exception:
            return {
                "phone_number": phone,
                "subscriber_tier": "FALLBACK_TUNNEL",
                "historical_fraud_reports": 0,
                "is_trusted": True
            }