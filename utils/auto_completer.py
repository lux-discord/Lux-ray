from disnake import ApplicationCommandInteraction

BOOL_CHOOSES = ["true", "false"]


async def bool_autocom(inter: ApplicationCommandInteraction, user_input: str = None):
    return (
        BOOL_CHOOSES
        if not user_input
        else [choose for choose in BOOL_CHOOSES if user_input.lower() in choose]
    )
