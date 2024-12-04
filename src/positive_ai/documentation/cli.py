from pathlib import Path
import click

from positive_ai.constants import SRC_DIR
from positive_ai.documentation.presentation import MemberOnboardingDeck, MemberInfo
from positive_ai.utils.click import SpecialHelpOrder


@click.group(cls=SpecialHelpOrder)
def cli():
    """Generates all the automatic documentation in english and french"""
    pass


@cli.command(
    help="Generate the employee starter presentation in english and french.",
    help_priority=1
)
@click.option(
    "--member-name",
    help="the name of the company joining positive AI",
    type=str,
    prompt=True,
)
@click.option(
    "--member-logo", help="the path to the member's logo", type=str, prompt=True
)
@click.option(
    "--member-join-month",
    help="the month the company joined positive AI",
    type=str,
    prompt=True,
)
@click.option(
    "--member-gatherer-firstname",
    help="the firstname of the company gatherer",
    type=str,
    prompt=True,
)
@click.option(
    "--member-gatherer-lastname",
    help="the lastname of the company gatherer",
    type=str,
    prompt=True,
)
@click.option(
    "--member-gatherer-email",
    help="the email address of the company gatherer",
    type=str,
    prompt=True,
)
@click.option(
    "--member-gatherer-photo",
    help="the email address of the company gatherer",
    type=str,
    prompt=False,
)
def generate_one_flyer(
    member_name,
    member_logo,
    member_join_month,
    member_gatherer_firstname,
    member_gatherer_lastname,
    member_gatherer_email,
    member_gatherer_photo,
):
    # Summarise member info from prompt
    infos = MemberInfo(
        member_name=member_name.capitalize(),
        member_logo_path=member_logo,
        member_join_month=member_join_month,
        member_gatherer_firstname=member_gatherer_firstname.capitalize(),
        member_gatherer_lastname=member_gatherer_lastname.capitalize(),
        member_gatherer_email=member_gatherer_email.lower(),
        member_gatherer_photo_path=member_gatherer_photo,
    )


    # Build french deck
    print("[+] Generating french doc...")
    fr_template_path = (
        SRC_DIR / "templates" / "2024_09 Positive_AI_Flyer membres-template-fr.pptx"
    )
    french_deck = MemberOnboardingDeck(
        template_path=fr_template_path, infos=infos, language="fr"
    )
    filename = f"2024_09_Positive_AI_Flyer_{infos.member_id}_fr.pptx"
    french_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / infos.member_id
        / "employee-onboarding"
        / filename
    )

    # Build english deck
    print("[+] Generating english doc...")
    en_template_path = (
        SRC_DIR / "templates" / "2024_09 Positive_AI_Flyer membres-template-en.pptx"
    )
    english_deck = MemberOnboardingDeck(
        template_path=en_template_path, infos=infos, language="en"
    )
    filename = f"2024_09_Positive_AI_Flyer_{infos.member_id}_en.pptx"
    english_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / infos.member_id
        / "employee-onboarding"
        / filename
    )

    print("[+] Done.")


@cli.command(
    help="Batch generate all the employee starter presentation in english and french.",
    help_priority=2
)
@click.option(
    "--config-file-path",
    help="configuration file holding all necessary information about joining members",
    type=str,
    prompt=True,
)
def generate_all_flyers(config_file_path):
    pass