from datetime import datetime
from .data_items import OuterContextItem


def make_session_id() -> str:
    return f"{datetime.now():%y%m%d%H%M%S}"


def make_name(outer_context: OuterContextItem, dirty=True, short=False) -> str:
    if short:
        return f"{outer_context.UserId}_{outer_context.SessionId}_{outer_context.ClientId}"
    long = f"user_{outer_context.UserId}_session_{outer_context.SessionId}_client_{outer_context.ClientId}"
    if dirty:
        return f"{long}.json"
    return f"{long}_clean.json"
