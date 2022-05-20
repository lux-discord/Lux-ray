from typing import TYPE_CHECKING

from disnake import ApplicationCommandInteraction

from core.language import GLOBAL_SUPPORT_LANGUAGE

if TYPE_CHECKING:
    from typing import Iterable, Mapping

BOOL_CHOOSES = ["true", "false"]


def choose_list_generater(chooses: "Iterable[str]", user_input: str):
    return (
        list(chooses)
        if not user_input
        else [choose for choose in chooses if user_input.lower() in choose]
    )


def choose_mapping_generater(chooses: "Mapping[str, str]", user_input: str):
    return (
        dict(chooses)
        if not user_input
        else {
            choose: value
            for choose, value in chooses.items()
            if user_input.lower() in choose
        }
    )


async def bool_autocom(inter: ApplicationCommandInteraction, user_input: str = None):
    return choose_list_generater(BOOL_CHOOSES, user_input)


async def lang_code_autocom(
    inter: ApplicationCommandInteraction,
    user_input: str = None,
    *,
    support_language: "Iterable[str]" = GLOBAL_SUPPORT_LANGUAGE,
):
    return choose_list_generater(support_language, user_input)
