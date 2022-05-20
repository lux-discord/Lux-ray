BOT_COLOR = 0x66E8E4


def embed_setup(embed, *, fields: list, image_url=None):
    if fields:
        for field in fields:
            if len(field) == 3:
                name, value, inline = field
                embed.add_field(name=name, value=value, inline=inline)
            else:
                name, value = field
                embed.add_field(name=name, value=value)

    if image_url:
        embed.set_image(url=image_url)

    return embed
