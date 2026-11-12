"""Small shared bits: escaping, number checks, the Cillian easter egg."""
import html
import re
from urllib.parse import urlencode


class UserError(Exception):
    pass


def esc(value):
    return html.escape(str(value), quote=True)


# easter egg: Cillian gets highlighted
EGG_PATTERN = re.compile(r"\b(cillian)\b", re.IGNORECASE)
secret_Img = '<img class="trophy" src="spongebob" alt="Animation">'


def name_html(name):
    parts = EGG_PATTERN.split(str(name))
    return "".join(f'<mark class="egg">{esc(p)}</mark>{secret_Img}' if i % 2 else esc(p)
                   for i, p in enumerate(parts))


def back(path, **params):
    clean = {k: v for k, v in params.items() if v not in (None, "")}
    return path + ("?" + urlencode(clean) if clean else "")


def to_int(value, label, minimum=0, maximum=100000):
    try:
        number = int(str(value).strip())
    except ValueError:
        raise UserError(f"{label} must be a whole number.")
    if number < minimum or number > maximum:
        raise UserError(f"{label} must be between {minimum} and {maximum}.")
    return number


def positive_or(value, default):
    try:
        number = int(value)
        return number if number >= 1 else default
    except (TypeError, ValueError):
        return default


def clean_name(value):
    return " ".join(str(value).split())[:60]
