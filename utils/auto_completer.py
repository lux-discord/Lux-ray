from disnake import ApplicationCommandInteraction


async def bool_autocom(inter: ApplicationCommandInteraction, user_input: str = None):
    chooses = ["True", "False"]
    if not user_input:
        return chooses
    return [choose for choose in chooses if user_input.capitalize() in chooses]
