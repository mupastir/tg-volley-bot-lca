from translate import Translator as Translator_


class Translator(Translator_):
    def __init__(self) -> None:
        super().__init__(to_lang="en", from_lang="ru")


translator = Translator()
