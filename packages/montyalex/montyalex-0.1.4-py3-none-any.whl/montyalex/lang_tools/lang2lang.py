from googletrans import LANGCODES, Translator

from montyalex.console_tools import richconsole
from montyalex.typing_tools import Any

translator = Translator()
print = richconsole.print


def lang(s: str, *, trg: str = "en", src: str = "auto") -> str:
    return translator.translate(s, dest=trg, src=src).text


def language_codes() -> dict[Any, Any]:
    return LANGCODES


language_codes_dict: dict[Any, Any] = language_codes()
langcodes: callable = language_codes
langcodes_dict: dict[Any, Any] = langcodes()


def language(
    string: str, *, target: str = "en", source: str = "auto"
) -> str:
    return lang(string, trg=target, src=source)


# ----------------------------------------------------------------------
# | Example Usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print(lang("Hello", trg="fr"))
    print(lang("Hello", trg="it"))
    print(lang("Hello", trg="de"))
