from datetime import datetime
from pathlib import Path
import click

from constants import ROOT_DIR
from src.employee_guide.presentation import MemberOnboardingDeck, MemberInfo


@click.group()
def cli():
    """List of commands bellow"""
    pass


@cli.command(
    help="Generate the employee starter presentation in english and french.",
    #help_priority=1
)
@click.option('--member-name',
              help="the name of the company joining positive AI",
              type=str,
              prompt=True
              )
@click.option('--member-join-month',
              help="the month the company joined positive AI",
              type=str,
              prompt=True
              )
@click.option('--member-gatherer-firstname',
              help="the firstname of the company gatherer",
              type=str,
              prompt=True
              )
@click.option('--member-gatherer-lastname',
              help="the lastname of the company gatherer",
              type=str,
              prompt=True
              )
@click.option('--member-gatherer-email',
              help="the email address of the company gatherer",
              type=str,
              prompt=True
              )
def generate(member_name, member_join_month, member_gatherer_firstname, member_gatherer_lastname, member_gatherer_email):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Summarise member info from prompt
    infos = MemberInfo(member_name=member_name,
                       member_join_month=member_join_month,
                       member_gatherer_firstname=member_gatherer_firstname,
                       member_gatherer_lastname=member_gatherer_lastname,
                       member_gatherer_email=member_gatherer_email)

    # Build french deck
    fr_template_path = ROOT_DIR / "templates" / "2024_09 Positive_AI_Flyer membres-template-fr.pptx"
    french_deck = MemberOnboardingDeck(template_path=fr_template_path, infos=infos)
    filename = f"2024_09_Positive_AI_Flyer_{infos.member_name.lower()}_fr.pptx"
    french_deck.save(file_path=Path.cwd() / "positive-ai-generated" / "employee-onboarding" / filename)
