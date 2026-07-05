from dataclasses import dataclass
from datetime import datetime


@dataclass
class Match:
    uid: str
    date: datetime
    title: str
    category: str
    system: str
    info: str
    location: str
    start_time: str
    age: str
    notes: str

    @property
    def description(self) -> str:
        parts = []

        if self.system:
            parts.append(f"Systeem: {self.system}")

        if self.info:
            parts.append(f"Informatie:\n{self.info}")

        if self.age:
            parts.append(f"Leeftijd:\n{self.age}")

        if self.notes:
            parts.append(f"Overige informatie:\n{self.notes}")

        return "\n\n".join(parts)
