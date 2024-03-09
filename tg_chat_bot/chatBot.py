from aiogram import Bot, Router, filters
from opentele.tl import TelegramClient
from opentele.td import TDesktop
from opentele.api import UseCurrentSession, CreateNewSession
from telethon import events 

import json as js
from typing import Dict


class aiogramChatBot:
    __settings: str
    __bot: Bot
    __router: Router
    __commands: Dict[str, any] = {}

    # TODO: #66 make dataclass command with command:str callback:funcpointer and role:eql_queries.Role
    @property
    def bot(self):
        return self.__bot

    @property
    def router(self):
        return self.__router

    @property
    def settings(self):
        return self.__settings

    def __init__(
        self,
        settings: str,
        router_name: str | None = None,
        *routers: Router,
    ) -> None:
        parmsFileDes = open(settings, "r")
        params = js.load(parmsFileDes)
        api_token = params["api_key"]
        self.__bot = Bot(token=api_token)
        self.__router = Router(name=router_name if router_name is not None else "")
        if len(routers) > 0:
            self.__router.include_routers(routers)
        self.__settings = settings

    def init_commands(self, callbacks: Dict[str, any]) -> None:
        self.__commands = callbacks
        for key, val in self.__commands.items():
            self.router.message.register(val, filters.Command(key))


class openteleChatBot(TelegramClient):
    __desktop: TDesktop
    __tdata: str

    @property
    def desktop(self):
        return self.__desktop
    
    @property

    async def __init__(self, tdata: str = "") -> None:
        if self.test_tdata(tdata):
            self.__tdata = tdata
            self.__desktop = TDesktop(tdata)
            self.__client = await self.__desktop.ToTelethon(session="telethon.session", flag=UseCurrentSession)
        else:
            raise Exception("tdata is not valid")
   

    def init_commands(self, callbacks: Dict[str, any]) -> None:
        for key, val in callbacks.items():
            self.add_event_handler(val, events.NewMessage(pattern=key))
            
    async def test_tdata(self, tdata: str) -> bool:
        desktop = TDesktop(tdata)
        # if it is loaded and accounts more then 0 then try to connect
        result = desktop.isLoaded() and (desktop.accountsCount > 0)
        if result:
            client = await desktop.ToTelethon(session="telethon.session", flag=CreateNewSession)
            try:
                client.connect()
            except OSError:
                # if we cannot connect to telegram - we cannot say what tdata is ok
                result = False
        return result
    
    
