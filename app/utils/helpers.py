import re


def clean_slug(slug: str) -> str:
    return re.sub(r"[^a-zA-Z0-9-_]", "", slug)


def create_slug(title: str) -> str:
    return clean_slug("-".join(title.lower().strip().split()))
