from app import MiniGramUpdate


def get_update_event(text: str):
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 3,
                "date": 1,
                "text": text,
                "chat": {
                    "id": 1,
                    "type": "private",
                },
                "user": {
                    "id": 1,
                },
                "from": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
                },
            },
        }
    )
