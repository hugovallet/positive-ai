import datetime
from pathlib import Path
import click
import yaml

from positive_ai.constants import SRC_DIR
from positive_ai.documentation.employee_flyer import MemberOnboardingDeck
from positive_ai.documentation.community_deck import CommunityDeck
from positive_ai.documentation.data_model import MemberInfo, AllMembersInfo
from positive_ai.utils.click import SpecialHelpOrder
from positive_ai.utils.io import read_yaml


@click.group(cls=SpecialHelpOrder)
def cli():
    """Generates all the automatic documentation in english and french"""
    pass


@cli.command(
    help="Generate the employee starter presentation in english and french.",
    help_priority=1,
)
@click.option(
    "--member-name",
    help="the name of the company joining positive AI",
    type=str,
    prompt=True,
)
@click.option(
    "--member-logo-path", help="the path to the member's logo", type=str, prompt=True
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
    "--member-gatherer-photo-path",
    help="the email address of the company gatherer",
    type=str,
    prompt=False,
)
def generate_one_flyer(
    member_name,
    member_logo_path,
    member_join_month,
    member_gatherer_firstname,
    member_gatherer_lastname,
    member_gatherer_email,
    member_gatherer_photo_path,
):
    ts = datetime.datetime.now().strftime("%Y_%m_%d")

    # Summarise member info from prompt
    infos = MemberInfo(
        member_name=member_name,
        member_logo_path=member_logo_path,
        member_join_month=member_join_month,
        member_gatherer_firstname=member_gatherer_firstname.capitalize(),
        member_gatherer_lastname=member_gatherer_lastname.capitalize(),
        member_gatherer_email=member_gatherer_email.lower(),
        member_gatherer_photo_path=member_gatherer_photo_path,
    )
    print(f"[+] Generating doc for member '{infos.member_name}'")

    # Build french deck
    print("[+] Generating french doc...")
    fr_template_path = (
        SRC_DIR / "templates" / "2024_09 Positive_AI_Flyer membres-template-fr.pptx"
    )
    french_deck = MemberOnboardingDeck(
        template_path=fr_template_path, infos=infos, language="fr"
    )
    filename = f"{ts}_Positive_AI_Flyer_{infos.member_id}_fr.pptx"
    french_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "member-specific"
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
    filename = f"{ts}_Positive_AI_Flyer_{infos.member_id}_en.pptx"
    english_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "member-specific"
        / infos.member_id
        / "employee-onboarding"
        / filename
    )

    print("[+] Done.")


@cli.command(
    help="Batch generate all the employee starter presentation in english and french.",
    help_priority=2,
)
@click.option(
    "--config-file-path",
    help="configuration file holding all necessary information about joining members",
    type=str,
    prompt=True,
)
def generate_all_flyers(config_file_path):
    print("[+] Starting batch flyer generation...")
    with open(config_file_path) as stream:
        try:
            loaded = yaml.safe_load(stream)
            for member_config in loaded:
                try:
                    params = [p.name for p in generate_one_flyer.params]
                    generate_one_flyer.callback(
                        **{k: v for k, v in member_config.items() if k in params}
                    )
                except Exception as e:
                    raise e

        except yaml.YAMLError as exc:
            raise exc


@cli.command(
    help="Batch generate all the employee starter presentation in english and french.",
    help_priority=2,
)
@click.option(
    "--config-file-path",
    help="configuration file holding all necessary information about joining members",
    type=str,
    prompt=True,
)
def generate_community_deck(config_file_path):
    ts = datetime.datetime.now().strftime("%Y_%m_%d")
    infos = AllMembersInfo(all_members_info=read_yaml(config_file_path))

    # Build english deck
    print("[+] Generating french doc...")
    fr_template_path = (
        SRC_DIR / "templates" / "Ateliers-pai-trombinoscope-template.pptx"
    )
    fr_deck = CommunityDeck(
        template_path=fr_template_path, infos=infos, language="fr"
    )
    filename = f"{ts}_Positive_AI_Community_Deck_fr.pptx"
    fr_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "non-member-specific"
        / filename
    )

    print("[+] Generating english doc...")
    en_template_path = (
        SRC_DIR / "templates" / "Ateliers-pai-trombinoscope-template.pptx"
    )
    english_deck = CommunityDeck(
        template_path=en_template_path, infos=infos, language="en"
    )
    filename = f"{ts}_Positive_AI_Community_Deck_en.pptx"
    english_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "non-member-specific"
        / filename
    )

    print("[+] Done.")
