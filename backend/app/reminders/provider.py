"""SMS provider interface and a fake implementation for development and tests (no network)."""
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class SendResult:
    ok: bool
    transient: bool = False  # only meaningful when ok is False: True means "worth retrying"
    error: str | None = None


class SmsProvider(Protocol):
    def send(self, to: str, body: str) -> SendResult: ...


@dataclass
class FakeSmsProvider:
    """Records messages instead of sending them.

    Script outcomes by putting SendResult values in `queue`; each `send` consumes one.
    With an empty queue every send succeeds.
    """

    sent: list[tuple[str, str]] = field(default_factory=list)
    queue: list[SendResult] = field(default_factory=list)
    calls: int = 0

    def send(self, to: str, body: str) -> SendResult:
        self.calls += 1
        result = self.queue.pop(0) if self.queue else SendResult(ok=True)
        if result.ok:
            self.sent.append((to, body))
        return result
