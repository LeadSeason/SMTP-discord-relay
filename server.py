from discord import Webhook, AsyncWebhookAdapter
import discord
from aiosmtpd.controller import Controller

import aiohttp
import asyncio
import logging
import datetime

url = "<set discord web hook here>"


class RelayHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        print(address + " " + "is added to rcpt_tos")

        # Make an envelope for the recipient with the same content.
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        message_decoded = envelope.content.decode('utf8', errors='replace')

        for x in [message_decoded[i:i + 2000] for i in range(0, len(message_decoded), 2000)]:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                embed = discord.Embed(title=f'Message from {envelope.mail_from}', description=f"```{x}```", colour=0xffff)
                embed.set_footer(text=str(datetime.datetime.now()))

                await webhook.send(embed=embed, username="localmail", )

        return '250 Message will be delivered'


async def amain(loop):
    handler = RelayHandler()
    cont = Controller(handler, hostname='localhost', port=25)
    cont.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
