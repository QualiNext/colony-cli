import os
from typing import Dict, List

from colony.services.branding import Branding


class GlobalInputParser:
    def __init__(self, command_args: Dict):
        """
        Parses CLI args and environment variables for inputs that appear before the command
        :param command_args: command_args is expected to be initialized using doc_opt
        """
        self._args = command_args

    @property
    def token(self) -> str:
        return self._args.get("--token", None) or os.environ.get(f"{Branding.env_var_prefix()}_TOKEN", None)

    @property
    def space(self) -> str:
        return self._args.get("--space", None) or os.environ.get(f"{Branding.env_var_prefix()}_SPACE", None)

    @property
    def account(self) -> str:
        return self._args.get("--account", None) or os.environ.get(f"{Branding.env_var_prefix()}_ACCOUNT", None)

    @property
    def profile(self) -> str:
        return self._args.get("--profile", None)

    @property
    def debug(self) -> str:
        return self._args.get("--debug", None)

    @property
    def command(self) -> str:
        return self._args.get("<command>", None)

    @property
    def command_args(self) -> List[str]:
        return self._args.get("<args>", None)

    @staticmethod
    def get_config_path() -> str:
        return os.environ.get(f"{Branding.env_var_prefix()}_CONFIG_PATH", None)
