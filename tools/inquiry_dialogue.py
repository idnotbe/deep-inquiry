"""Deterministic, bounded access to frozen records; no grading or model calls."""
from dataclasses import dataclass, field
import re
from typing import TypeAlias

JsonValue: TypeAlias = None | bool | int | float | str | list['JsonValue'] | dict[str, 'JsonValue']


class DialogueError(RuntimeError):
    """An invalid specification or interaction, never evidence of difficulty."""


@dataclass(slots=True)
class Dialogue:
    """Per-trial mutable request budget and terminal state."""
    records: dict[str, str]
    max_requests: int
    requests: list[str] = field(default_factory=list)
    finished: bool = False

    @classmethod
    def parse(cls, value: JsonValue) -> 'Dialogue':
        """Parse the suite-owned specification without exposing it to a model."""
        if not isinstance(value, dict) or set(value) != {'records', 'max_requests'}:
            raise DialogueError('invalid dialogue specification')
        records, limit = value['records'], value['max_requests']
        if not isinstance(records, dict) or not records or type(limit) is not int or not 1 <= limit <= 8:
            raise DialogueError('invalid records or request limit')
        parsed: dict[str, str] = {}
        for key, text in records.items():
            if not re.fullmatch(r'[A-Za-z0-9_-]+', key) or not isinstance(text, str) or not text.strip():
                raise DialogueError('invalid record key or text')
            parsed[key] = text
        return cls(parsed, limit)

    def reply(self, response: str) -> str | None:
        """Deliver exactly one requested record; ordinary prose ends the trial."""
        if self.finished:
            raise DialogueError('dialogue already finalized')
        text = response.strip()
        if not re.match(r'^[`*_#>\-]*\s*read\b', text, re.IGNORECASE):
            self.finished = True
            return None
        if not re.fullmatch(r'READ [A-Za-z0-9_-]+', text):
            raise DialogueError('malformed record request')
        key = text[5:]
        if key not in self.records or len(self.requests) >= self.max_requests:
            raise DialogueError('unknown record or request budget exhausted')
        self.requests.append(key)
        return self.records[key]
