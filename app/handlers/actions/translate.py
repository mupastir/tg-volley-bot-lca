from app.misc.translator import translator


def translate_handler(q: str) -> str:
    return translator.translate(q)
