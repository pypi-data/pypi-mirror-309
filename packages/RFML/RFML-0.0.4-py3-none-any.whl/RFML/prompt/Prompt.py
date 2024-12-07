from enum import Enum
from RFML.core.Hosts import HTTPHost, CLIHost
from RFML.interface.IPrompt import IPrompt


class Interface(Enum):
    API = 1
    CLI = 2


class Prompt:
    interface = Interface.CLI
    handler = any

    def __init__(self, interface: Interface, handler: IPrompt = None):
        self.interface = interface
        self.handler = handler

    def invoke_prompt(self, library_prompt_callback):
        if self.interface == Interface.API:
            print("API Host has been attached")
            HTTPHost(
                self.handler,  # client handler
                library_prompt_callback  # FW callback
            )
        if self.interface == Interface.CLI:
            print("CLI Host has been attached")
            CLIHost(self.handler, library_prompt_callback)
