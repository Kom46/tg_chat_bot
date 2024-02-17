from aiogram import Bot, Router, filters


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
