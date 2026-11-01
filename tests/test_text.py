from app import text


def test_slugify():
    assert text.slugify("  Hello, World!  ") == "hello-world"
    assert text.slugify("--Already--Slugged--") == "already-slugged"
    assert text.slugify("Café 2024") == "caf-2024"


def test_truncate():
    assert text.truncate("abcdefghij", 8) == "abcde..."
    assert len(text.truncate("abcdefghij", 8)) == 8
    assert text.truncate("short", 10) == "short"


def test_title_case():
    assert text.title_case("the lord of the rings") == "The Lord of the Rings"
    assert text.title_case("WAR AND PEACE") == "War and Peace"


def test_count_words():
    assert text.count_words("") == 0
    assert text.count_words("don't stop") == 2
    assert text.count_words("state-of-the-art   design ") == 2


def test_reverse_words():
    assert text.reverse_words("one two three") == "three two one"
    assert text.reverse_words("  hello   world ") == "world hello"


def test_is_palindrome():
    assert text.is_palindrome("A man, a plan, a canal: Panama")
    assert text.is_palindrome("Racecar")
    assert not text.is_palindrome("hello")


def test_camel_to_snake():
    assert text.camel_to_snake("userId") == "user_id"
    assert text.camel_to_snake("HTTPResponseCode") == "http_response_code"
    assert text.camel_to_snake("parseJSON") == "parse_json"


def test_snake_to_camel():
    assert text.snake_to_camel("user_id") == "userId"
    assert text.snake_to_camel("http_response_code") == "httpResponseCode"
    assert text.snake_to_camel("single") == "single"


def test_pad_left():
    assert text.pad_left("42", 5) == "00042"
    assert text.pad_left("7", 3, " ") == "  7"
    assert text.pad_left("123456", 3) == "123456"


def test_mask_email():
    assert text.mask_email("johndoe@example.com") == "j*****e@example.com"
    assert text.mask_email("ab@x.io") == "a*@x.io"


def test_initials():
    assert text.initials("ada lovelace") == "AL"
    assert text.initials("ada  lovelace") == "AL"
    assert text.initials(" grace brewster hopper ") == "GBH"
