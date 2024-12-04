from pathlib import Path
import click

from positive_ai.constants import SRC_DIR
from positive_ai.documentation.presentation import MemberOnboardingDeck, MemberInfo
from positive_ai.utils.click import SpecialHelpOrder


@click.group(cls=SpecialHelpOrder)
def cli():
    """All template emails to onboard new members"""
    pass


@cli.command(help="Send a welcome message in French or English", help_priority=1)
def send_welcome():
    pass
