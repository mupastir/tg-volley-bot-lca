def translate_handler(q: str) -> str:
    from app.main import translator

    return translator.translate(q)
