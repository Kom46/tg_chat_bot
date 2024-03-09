import os
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
    def settings(self):
        return self.__settings

    def __init__(
        self,
        settings: str | None = None,
        api_key: str | None = None,
        router_name: str | None = None,
        *routers: Router,
    ) -> None:
        if (settings is None) and (api_key is None):
            raise Exception("Nor settings nor api_key is provided")
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
            self.__router.message.register(val, filters.Command(key))


class openteleChatBot(TelegramClient):
    __tdata: str
    __session: str
    __client: TelegramClient
    

    @property
    def desktop(self):
        return self.__desktop
    
    @property
    def tdata(self):
        return self.__tdata
    
    async def __init__(self, tdata: str = "") -> None:
        if self.test_tdata(tdata):
            self.__tdata = tdata
            desktop = TDesktop(tdata)
            self.__client = await desktop.ToTelethon(session="telethon.session", flag=UseCurrentSession)
        else:
            raise Exception("tdata is not valid")
   

    def init_commands(self, callbacks: Dict[str, any]) -> None:
        for key, val in callbacks.items():
            self.add_event_handler(val, events.NewMessage(pattern=key))
            
    async def test_tdata(cls, tdata: str) -> bool:
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
    
    async def convert_tdata(cls, tdata: str, session_path: str = "telethon.session", flag: int = UseCurrentSession) -> str:
        result = ""
        if cls.test_tdata(tdata):
            desktop = TDesktop(tdata)
            desktop.ToTelethon(session=session_path, flag=flag)
            if os.path.exists(session_path):
                result = session_path
        return result
    
    async def get_proxy_from_file(self, filename: str) -> bool:
        pass
    
    async def get_proxy_from_database(self, database: str) -> bool:
        pass
    
    async def test_proxy(ip: str, port: int) -> bool:
        pass
    
    def add_event_handler(self, callback: any, event: events.NewMessage, trigger: str = "") -> None:
        result = True
        if trigger != "":
            event = events.NewMessage(pattern=trigger)
        self.__client.add_event_handler(callback, event)
        return result
    
    def start(self) -> None:
        self.__client.run_until_disconnected()
    
    def stop(self) -> None:
        self.__client.disconnect()
