import datetime
from pathlib import Path
import click
import yaml

from positive_ai.constants import SRC_DIR
from positive_ai.documentation.core_team_deck import CoreTeamDeck
from positive_ai.documentation.employee_flyer import MemberOnboardingDeck
from positive_ai.documentation.community_deck import CommunityDeck
from positive_ai.documentation.data_model import (
    MemberInfo,
    AllMembersInfo,
    AllCoreTeamMembersInfo,
    BaseMemberInfo,
)
from positive_ai.documentation.referent_starter_pack import ReferentStarterPack
from positive_ai.utils.click import SpecialHelpOrder
from positive_ai.utils.io import read_yaml


@click.group(cls=SpecialHelpOrder)
def cli():
    """Generates all the automatic documentation in english and french"""
    pass


@cli.command(
    help="Generate the full starter pack in english and french for a new company",
    help_priority=0,
)
@click.option(
    "--member-name",
    help="Name of the company joining Positive AI",
    type=str,
    prompt="Please provide the full name of the company joining Positive AI",
)
def generate_starter_pack(member_name):
    ts = datetime.datetime.now().strftime("%Y_%m_%d")
    infos = BaseMemberInfo(member_name=member_name)

    # Build english deck
    print("[+] Generating french doc...")
    fr_template_path = SRC_DIR / "templates" / "pai_starter_pack_v2_fr.pptx"
    fr_deck = ReferentStarterPack(
        template_path=fr_template_path, infos=member_name, language="fr"
    )
    filename = f"{ts}_Positive_AI_Starter_Pack_{infos.member_id}_fr.pptx"
    fr_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "member-specific"
        / infos.member_id
        / "referent-onboarding"
        / filename
    )

    # print("[+] Generating english doc...")
    # en_template_path = SRC_DIR / "templates" / "2024_12_PAI_starter_pack_en.pptx"
    # english_deck = ReferentStarterPack(
    #     template_path=en_template_path, infos=member_name, language="en"
    # )
    # filename = f"{ts}_Positive_AI_Starter_Pack_{infos.member_id}_en.pptx"
    # english_deck.save(
    #     file_path=Path.cwd()
    #     / "positive_ai-generated"
    #     / "non-member-specific"
    #     / filename
    # )

    print("[+] Done.")


@cli.command(
    help="Generate the employee flyer in english and french for one company",
    help_priority=1,
)
@click.option(
    "--member-name",
    help="the name of the company joining positive AI",
    type=str,
    prompt="Company joining positive AI name",
)
@click.option(
    "--member-logo-path",
    help="the path to the member's logo",
    type=str,
    prompt="Please provide the path to the logo image of the company",
    prompt_required=True,
)
@click.option(
    "--member-join-month",
    help="the month the company joined positive AI",
    type=str,
    prompt="Please provide the month, year the company joined positive AI",
)
@click.option(
    "--member-gatherer-firstname",
    help="the firstname of the company gatherer",
    type=str,
    prompt="Please provide the first name of the company referent",
)
@click.option(
    "--member-gatherer-lastname",
    help="the lastname of the company gatherer",
    type=str,
    prompt="Please provide the last name of the company referent",
)
@click.option(
    "--member-gatherer-email",
    help="the email address of the company gatherer",
    type=str,
    prompt="Please provide the email address of the company referent",
)
@click.option(
    "--member-gatherer-photo-path",
    help="the email address of the company gatherer",
    type=str,
    prompt="Please provide the path to the professional photo of the company referent",
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
        SRC_DIR / "templates" / "2024_09_pai_members_flyer_template_fr.pptx"
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
        SRC_DIR / "templates" / "2024_09_pai_members_flyer_template-en.pptx"
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
    help="Generate ALL the employee flyers in english and french from structured member data",
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
    help="Generate community facebook in english and french.",
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
    fr_template_path = SRC_DIR / "templates" / "pai_slide_master.pptx"
    fr_deck = CommunityDeck(template_path=fr_template_path, infos=infos, language="fr")
    filename = f"{ts}_Positive_AI_Community_Deck_fr.pptx"
    fr_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "non-member-specific"
        / filename
    )

    print("[+] Generating english doc...")
    en_template_path = SRC_DIR / "templates" / "pai_slide_master.pptx"
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


@cli.command(
    help="Generate core team facebook in english and french.",
    help_priority=3,
)
@click.option(
    "--config-file-path",
    help="configuration file holding all necessary information about joining members",
    type=str,
    prompt=True,
)
def generate_core_team_deck(config_file_path):
    ts = datetime.datetime.now().strftime("%Y_%m_%d")
    infos = AllCoreTeamMembersInfo(all_members_info=read_yaml(config_file_path))

    # Build english deck
    print("[+] Generating french doc...")
    fr_template_path = SRC_DIR / "templates" / "pai_slide_master.pptx"
    fr_deck = CoreTeamDeck(template_path=fr_template_path, infos=infos, language="fr")
    filename = f"{ts}_Positive_AI_Core_Team_Deck_fr.pptx"
    fr_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "non-member-specific"
        / filename
    )

    print("[+] Generating english doc...")
    en_template_path = SRC_DIR / "templates" / "pai_slide_master.pptx"
    english_deck = CoreTeamDeck(
        template_path=en_template_path, infos=infos, language="en"
    )
    filename = f"{ts}_Positive_AI_Core_Team_Deck_en.pptx"
    english_deck.save(
        file_path=Path.cwd()
        / "positive_ai-generated"
        / "non-member-specific"
        / filename
    )

    print("[+] Done.")
