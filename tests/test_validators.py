from app import validators as v


def test_is_valid_email():
    assert v.is_valid_email("user@example.com")
    assert not v.is_valid_email("user@example.com<script>")
    assert not v.is_valid_email("no-at-sign.com")
    assert not v.is_valid_email("a@b.c")


def test_is_valid_hex_color():
    assert v.is_valid_hex_color("#FFF")
    assert v.is_valid_hex_color("#a1b2c3")
    assert not v.is_valid_hex_color("#abcd")
    assert not v.is_valid_hex_color("123456")


def test_is_strong_password():
    assert v.is_strong_password("Abcdefg1")
    assert not v.is_strong_password("abcdefg1")
    assert not v.is_strong_password("Abcdefgh")
    assert not v.is_strong_password("Ab1")


def test_is_valid_ipv4():
    assert v.is_valid_ipv4("192.168.1.1")
    assert v.is_valid_ipv4("255.255.255.255")
    assert not v.is_valid_ipv4("256.1.1.1")
    assert not v.is_valid_ipv4("01.2.3.4")
    assert not v.is_valid_ipv4("1.2.3")


def test_is_valid_username():
    assert v.is_valid_username("alice_01")
    assert v.is_valid_username("a" * 16)
    assert not v.is_valid_username("1alice")
    assert not v.is_valid_username("ab")
    assert not v.is_valid_username("a" * 17)


def test_is_valid_us_zip():
    assert v.is_valid_us_zip("12345")
    assert v.is_valid_us_zip("12345-6789")
    assert not v.is_valid_us_zip("1234")
    assert not v.is_valid_us_zip("12345-678")


def test_luhn_check():
    assert v.luhn_check("4111 1111 1111 1111")
    assert v.luhn_check("79927398713")
    assert not v.luhn_check("4111 1111 1111 1112")
    assert not v.luhn_check("79927398710")


def test_is_valid_e164():
    assert v.is_valid_e164("+14155552671")
    assert not v.is_valid_e164("14155552671")
    assert not v.is_valid_e164("+0123456789")
    assert not v.is_valid_e164("+1234")


def test_is_valid_url():
    assert v.is_valid_url("https://example.com/path?q=1")
    assert v.is_valid_url("http://localhost:8000")
    assert not v.is_valid_url("ftp://example.com")
    assert not v.is_valid_url("http://")


def test_is_valid_isbn10():
    assert v.is_valid_isbn10("0-306-40615-2")
    assert v.is_valid_isbn10("0-8044-2957-X")
    assert not v.is_valid_isbn10("0-306-40615-3")
    assert not v.is_valid_isbn10("123")


def test_is_valid_uuid():
    assert v.is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")
    assert v.is_valid_uuid("123E4567-E89B-12D3-A456-426614174000")
    assert not v.is_valid_uuid("123e4567e89b12d3a456426614174000")
    assert not v.is_valid_uuid("not-a-uuid")
