from app.gateways.openai import OpenAI


OPENAI_MODIFIERS = (
    "ai!",
    "gpt!",
    "openai!",
    "чат!",
)
SYSTEM_PROMPT = (
    "You are a chat bot of beach volleyball community. "
    "You answer with no more than 50 words, should be in English language"
)


async def ask_ai_handler(openai_: OpenAI, question: str) -> str:
    q = question.split("!", 1)[1].strip()
    return await openai_.easy_complete(q, SYSTEM_PROMPT)
