import sys

from docopt import DocoptExit, docopt

from colony.base import ResourceManager
from colony.client import ColonyClient
from colony.config import ColonyConnection
from colorama import Fore, Back, Style


class BaseCommand(object):
    """
    usage: colony
    """

    RESOURCE_MANAGER = ResourceManager

    def __init__(self, command_args: list, connection: ColonyConnection = None):
        if connection:
            self.client = ColonyClient(space=connection.space, token=connection.token, account=connection.account)
            self.manager = self.RESOURCE_MANAGER(client=self.client)
        else:
            self.client = None
            self.manager = None

        self.args = docopt(self.__doc__, argv=command_args)

    def execute(self):
        """Finds a subcommand passed to with command in
        object actions table and executes mapped method"""

        args = self.args

        actions_table = self.get_actions_table()

        for action in actions_table:
            if args.get(action, False):
                # call action
                actions_table[action]()
                break

        # if subcommand was specified without args (actions), just show usage
        raise DocoptExit

    def get_actions_table(self) -> dict:
        return {}

    @staticmethod
    def styled_text(style, message: str = "", newline=True):
        if message:
            sys.stdout.write(style + message)
            sys.stdout.write(Style.RESET_ALL)
        if newline:
            sys.stdout.write("\n")

    @staticmethod
    def error(message: str = ""):
        BaseCommand.styled_text(Fore.RED, message)
        sys.exit(1)

    @staticmethod
    def success(message: str = ""):
        BaseCommand.styled_text(Fore.GREEN, message)
        sys.exit()

    @staticmethod
    def die(message: str = ""):
        if message:
            sys.stderr.write(message)
            sys.stderr.write("\n")
        sys.exit(1)

    @staticmethod
    # Unimportant info that can be de-emphasized
    def fyi_info(message: str = ""):
        BaseCommand.styled_text(Style.DIM, message)

    @staticmethod
    # Something active is being performed
    def action_announcement(message: str = ""):
        BaseCommand.styled_text(Fore.YELLOW, message)

    @staticmethod
    # Unimportant info that can be de-emphasized
    def info(message: str = ""):
        BaseCommand.styled_text(Fore.LIGHTBLUE_EX, message)

    @staticmethod
    # Unimportant info that can be de-emphasized
    def important_value(prefix_message: str = "", value: str = ""):
        if prefix_message:
            BaseCommand.styled_text(Style.DIM, prefix_message, False)
        BaseCommand.styled_text(Fore.CYAN,value)

    @staticmethod
    def message(message: str = ""):
        sys.stdout.write(message)
        sys.stdout.write("\n")

    @staticmethod
    def url(prefix_message, message: str = ""):
        if prefix_message:
            BaseCommand.styled_text(Style.DIM, prefix_message, False)
        BaseCommand.styled_text(Fore.BLUE, message)
