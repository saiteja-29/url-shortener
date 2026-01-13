from datetime import datetime


def calculate_ttl(expires_at):
    if not expires_at:
        return 60 * 60 * 24 * 30  # 30 days

    ttl = int((expires_at - datetime.utcnow()).total_seconds())
    return max(ttl, 0)
