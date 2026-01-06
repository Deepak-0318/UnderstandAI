# core/structuring/models.py
from dataclasses import dataclass, field

@dataclass
class Sentence:
    sentence_id: str
    text: str
    position: int

    metrics: dict = field(default_factory=dict)
    confusion_label: str | None = None
    explanation: str | None = None
