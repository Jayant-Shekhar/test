import hashlib
import hmac

from app import security


def test_sanitize_filename():
    assert security.sanitize_filename("../../etc/passwd") == "passwd"
    assert security.sanitize_filename("..\\..\\evil.sh") == "evil.sh"
    assert security.sanitize_filename("my report.pdf") == "my_report.pdf"
    assert security.sanitize_filename("...") == "file"


def test_safe_compare(monkeypatch):
    calls = []
    real = hmac.compare_digest

    def spy(a, b):
        calls.append((a, b))
        return real(a, b)

    monkeypatch.setattr(security.hmac, "compare_digest", spy)
    assert security.safe_compare("abc", "abc")
    assert not security.safe_compare("abc", "abd")
    assert calls, "secrets must be compared with hmac.compare_digest"


def test_hash_password():
    assert security.hash_password("pw", "s1") != security.hash_password("pw", "s2")
    expected = hashlib.pbkdf2_hmac("sha256", b"pw", b"salt", 1000).hex()
    assert security.hash_password("pw", "salt", 1000) == expected


def test_parse_bearer_token():
    assert security.parse_bearer_token("Bearer abc123") == "abc123"
    assert security.parse_bearer_token("bearer abc123") == "abc123"
    assert security.parse_bearer_token("Basic abc123") is None
    assert security.parse_bearer_token(None) is None


def test_redact_secrets():
    assert security.redact_secrets("password=hunter2 user=bob") == "password=*** user=bob"
    assert security.redact_secrets("API_KEY: abc123") == "API_KEY: ***"


def test_is_safe_redirect():
    allowed = {"example.com"}
    assert security.is_safe_redirect("/dashboard", allowed)
    assert security.is_safe_redirect("https://example.com/x", allowed)
    assert not security.is_safe_redirect("https://evilexample.com", allowed)
    assert not security.is_safe_redirect("javascript:alert(1)", allowed)
    assert not security.is_safe_redirect("//evil.com", allowed)


def test_has_permission():
    assert security.has_permission("editor", "editor")
    assert security.has_permission("admin", "viewer")
    assert not security.has_permission("viewer", "editor")
    assert not security.has_permission("guest", "viewer")


def test_rate_limiter():
    limiter = security.RateLimiter(limit=2, window=1.0)
    assert limiter.allow("k", 0.0)
    assert limiter.allow("k", 0.1)
    assert not limiter.allow("k", 0.2)
    assert limiter.allow("other", 0.2)
    assert limiter.allow("k", 1.0)


def test_mask_card_number():
    assert security.mask_card_number("4111-1111-1111-1234") == "**** **** **** 1234"


def test_generate_csrf_token():
    expected = hmac.new(b"server-secret", b"session-1", hashlib.sha256).hexdigest()
    assert security.generate_csrf_token("server-secret", "session-1") == expected


def test_strip_tags():
    html = "<p>Hi <b>there</b></p><script>alert(1)</script><style>p{}</style>"
    assert security.strip_tags(html) == "Hi there"
