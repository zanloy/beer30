# StdLib
from asyncio import sleep
import logging
from typing import List, Type

# Internal Deps
from .light import Light

# External Deps
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_sdk.models.blocks import Block, DividerBlock, HeaderBlock, SectionBlock
from slack_sdk.models.blocks.basic_components import MarkdownTextObject, PlainTextObject

class Bot:
    """A slack bot for beer30."""
    LIGHTS = {
        'red': ':red_circle:',
        'yellow': ':large_yellow_circle:',
        'green': ':large_green_circle:',
    }

    def __init__(self, token: str, light: Light, admins: List[str]=[]) -> None:
        # Validate
        if token == None or token == '':
            raise ValueError('token cannot be None or empty string')

        self._app = AsyncApp(token=token)
        self.token = token
        self._light = light
        self._admins = admins

        # Setup handlers
        self._app.event('app_mention')(self.handle_mention)
        #self._app.event('message')(self.handle_message)

    async def start(self) -> None:
        handler = AsyncSocketModeHandler(self._app)
        while True:
            try:
                await handler.start_async()
            except (ConnectionError, TimeoutError) as e:
                logging.error(e, f"connection error contacting Slack, waiting { self._wait } seconds to retry")
                await sleep(self._wait)
                continue

    async def cmd_help(self, event, text, say) -> None:
        """returns this help message"""
        (token, text) = self.next_token(text)
        if token == '':
            commands = []
            for cmd in self.commands():
                func = getattr(self, f"cmd_{cmd}")
                commands.append(f"{cmd}: {func.__doc__}")
            text = "\n".join(commands)
            await say(text)

    async def cmd_set(self, event, text, say) -> None:
        """sets the light color. eg: '@beer30 set green'"""
        if event['user'] not in self._admins:
            await say(f"Sorry <@{event['user']}> but you are not authorized to set the beer30 light.")
            return

        state, _ = self.next_token(text)
        if state == '':
            state = 'null'
        if state not in self._light.STATES:
            await say(f"Sorry <@{event['user']}> but {state} is not a valid state. Valid states are: {', '.join(self._light.STATES)}.")
            return

        self._light.state = state
        await self.cmd_status(event, text, say)

    async def cmd_status(self, event, text, say) -> None:
        """say the currect status of the beer30 light"""
        text = f"Beer30 light is currently {self._light.state}."
        mrkdwn = f"{self.LIGHTS[self._light.state]} Beer30 light is currently *{self._light.state}*."

        blocks: List[Type[Block]] = []
        blocks.append(
            SectionBlock(
                text = MarkdownTextObject(
                    text = mrkdwn
                )
            )
        )
        await say(text, blocks)

    async def cmd_whoami(self, event, text, say) -> None:
        """reply to you with your Slack ID (used for configuration)"""
        await say(f"<@{event['user']}>, sounds like an existential crisis but to me, you'll always be {event['user']}.")

    def commands(self) -> List[str]:
        command_list = [func[len('cmd_'):] for func in dir(self) if callable(getattr(self, func)) and func.startswith('cmd_')]
        return command_list

    async def handle_mention(self, event, say) -> None:
        (cmd, text) = self.next_token(event['text'])
        try:
            method = getattr(self, f'cmd_{cmd}')
        except AttributeError:
            await say(f'{cmd}: Unknown command.')
            return
        await method(event, text, say)

    async def send_message(self, channel: str, text: str, blocks=[]):
        await self._app.client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=blocks,
        )

    def next_token(self, text: str):
        tokens = text.split(' ', maxsplit=1)
        while len(tokens) < 2:
            tokens.append('')
        token, text = tokens[0], tokens[1]
        if token.startswith('<') or token in ['of']:
            return self.next_token(text)
        return (token, text)