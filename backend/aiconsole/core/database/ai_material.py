from dataclasses import dataclass
from typing import Optional


@dataclass
class AIMaterial:
    """Material model for AI agents"""

    id: str
    name: str
    version: str
    usage: str
    content_type: str
    content: str
    default_status: str
