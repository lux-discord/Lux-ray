from typing import Union

from disnake import Interaction, Member, SyncWebhook, User, Webhook
from disnake.abc import Messageable

Author = Union[Member, User]
SendAble = Union[Interaction, SyncWebhook, Webhook, Messageable]
EphemeralSendAble = Union[Interaction, Webhook]
