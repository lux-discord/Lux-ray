from typing import Union

from disnake import Interaction, SyncWebhook, Webhook
from disnake.abc import Messageable

SendAble = Union[Interaction, SyncWebhook, Webhook, Messageable]
