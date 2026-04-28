def find_capital_letters(s: str) -> str:
    return ''.join([c for c in s if c.isupper()])