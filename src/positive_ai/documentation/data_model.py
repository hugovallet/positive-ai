from typing import Optional

from googletrans import Translator
from pydantic import BaseModel, EmailStr


class CoreTeamMemberInfo(BaseModel):
    ct_member_firstname: str
    ct_member_lastname: str
    ct_member_title_fr: str = ""
    ct_member_title_en: str = ""
    ct_member_email: EmailStr
    ct_member_photo_path: Optional[str] = None
    ct_member_is_board: bool


class MemberInfo(BaseModel):
    member_name: str
    member_join_month: str
    member_logo_path: Optional[str] = None
    member_gatherer_firstname: str
    member_gatherer_lastname: str
    member_gatherer_title_fr: str = ""
    member_gatherer_title_en: str = ""
    member_gatherer_desc_fr: str = ""
    member_gatherer_desc_en: str = ""
    member_gatherer_email: EmailStr
    member_gatherer_photo_path: Optional[str] = None

    @property
    def member_id(self) -> str:
        return self.member_name.lower().replace(" ", "_")

    # @property
    # def member_gatherer_desc_en(self) -> str:
    #     translator = Translator()
    #     return translator.translate('veritas lux mea', src='fr', dest="en").text


class AllMembersInfo(BaseModel):
    all_members_info: list[MemberInfo]


class AllCoreTeamMembersInfo(BaseModel):
    all_members_info: list[CoreTeamMemberInfo]
