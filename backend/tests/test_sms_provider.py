from app.reminders.provider import FakeSmsProvider, SendResult


def test_fake_provider_succeeds_and_records_the_message_by_default():
    provider = FakeSmsProvider()
    result = provider.send("+91-90000-00001", "hello")
    assert result == SendResult(ok=True)
    assert provider.sent == [("+91-90000-00001", "hello")]
    assert provider.calls == 1


def test_SPEC001_AC4_fake_provider_can_be_scripted_to_fail_transiently_then_succeed():
    provider = FakeSmsProvider(queue=[SendResult(ok=False, transient=True, error="503"), SendResult(ok=True)])
    first = provider.send("+91-90000-00001", "hello")
    second = provider.send("+91-90000-00001", "hello")
    assert (first.ok, first.transient) == (False, True)
    assert second.ok is True
    assert provider.calls == 2
    assert len(provider.sent) == 1  # a failed attempt delivers nothing


def test_SPEC001_AC5_fake_provider_can_be_scripted_to_fail_permanently():
    provider = FakeSmsProvider(queue=[SendResult(ok=False, transient=False, error="invalid number")])
    result = provider.send("12345", "hello")
    assert (result.ok, result.transient, result.error) == (False, False, "invalid number")
    assert provider.sent == []
