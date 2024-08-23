
from dataclasses import dataclass

@dataclass
class FStatus:
    is_stuck:bool
    status_count: int
    last_status: str
