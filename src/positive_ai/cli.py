# -*- coding: utf-8 -*-
""" CLI helper """

import os

import click

from positive_ai.constants import SRC_DIR


class CLI(click.MultiCommand):

    """
    Define the CLI commands by lookup inside the subdirectories.
    """

    def list_commands(self, ctx):
        """list commands from cli.py files in subdirectories"""
        plugins = []
        for dir_name in os.listdir(SRC_DIR):
            dir_path = SRC_DIR / dir_name
            if os.path.isdir(dir_path):
                for filename in os.listdir(dir_path):
                    if filename == "cli.py":
                        plugins.append(os.path.basename(dir_path))
        plugins.sort()
        return plugins

    def get_command(self, ctx, cmd_name):
        """get command from subdirectory"""
        commands = {}  # type: ignore
        filename = SRC_DIR / cmd_name / "cli.py"
        try:
            with open(filename) as file:
                code = compile(file.read(), filename, "exec")
                eval(code, commands, commands)  # pylint: disable=eval-used
            return commands["cli"]
        except Exception as e:
            raise e


@click.command(cls=CLI)
@click.version_option(version="0.1.12")
def main():
    """
    Welcome to Positive AI starter util! Find the executable commands bellow.
    """


if __name__ == "__main__":
    main()
