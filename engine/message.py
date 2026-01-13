from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Message:
    text: str = ""
    color: Optional[Tuple[int, int, int]] = None
