import hashlib
from functools import lru_cache
from mimetypes import guess_extension
from pathlib import Path
from typing import BinaryIO, Optional

from aiconsole.core.database.services import UserAvatarService
from aiconsole.core.database.services import UserProfileService as DBUserProfileService
from aiconsole.core.users.types import UserProfile
from aiconsole.utils.resource_to_path import resource_to_path

DEFAULT_AVATARS_PATH = "aiconsole.preinstalled.avatars"


class MissingFileName(Exception):
    """File name is missing"""


class UserProfileService:
    def __init__(self):
        self.db_service = DBUserProfileService()
        self.avatar_service = UserAvatarService()
        self._current_user_id: Optional[str] = None

    def get_profile(self, email: str | None = None) -> UserProfile:
        """Get user profile from database"""
        # For now, we'll use a default user ID if none is set
        user_id = self._current_user_id or "default_user"
        profile = self.db_service.get_profile(user_id)
        if profile is None:
            # Create a default profile if none exists
            return UserProfile(
                id=user_id, username="default", email=email, avatar_url=self.get_default_avatar(email), gravatar=False
            )
        return profile

    def save_avatar(
        self,
        file: BinaryIO,
        file_name: str | None = None,
        content_type: str | None = None,
    ) -> None:
        """Save avatar to database"""
        extension = guess_extension(content_type) if content_type else None
        if not file_name:
            if not extension:
                raise MissingFileName()
            file_name = f"avatar{extension}"

        # Get current user's profile
        current_profile = self.get_profile()

        # Save avatar to database
        self.avatar_service.save_avatar(
            user_id=current_profile.id, file=file, filename=file_name, content_type=content_type or "image/jpeg"
        )

        # Update profile with new avatar URL
        if current_profile.email:
            avatar_url = f"profile_image?img_filename={file_name}"
            self.db_service.save_avatar(email=current_profile.email, avatar_url=avatar_url)

    def get_avatar(self, img_filename: str) -> bytes:
        """Get avatar data from database"""
        current_profile = self.get_profile()
        avatar = self.avatar_service.get_avatar(current_profile.id, img_filename)
        if not avatar:
            return b""

        # Convert binary data to bytes
        return bytes(avatar.data) if isinstance(avatar.data, (bytes, bytearray)) else b""

    def get_default_avatar(self, email: str | None = None) -> str:
        """Get default avatar URL"""
        key = email or "some_key"
        img_filename = self._deterministic_choice(
            blob=key,
            choices=list(resource_to_path(resource=DEFAULT_AVATARS_PATH).glob(pattern="*")),
        ).name
        return f"profile_image?img_filename={img_filename}"

    def _deterministic_choice(self, blob: str, choices: list[Path]) -> Path:
        hash_value = hashlib.sha256(string=blob.encode()).hexdigest()
        choice_index = int(hash_value, base=16) % len(choices)
        return choices[choice_index]

    def set_current_user_id(self, user_id: str) -> None:
        """Set the current user ID"""
        self._current_user_id = user_id


@lru_cache
def user_profile_service() -> UserProfileService:
    return UserProfileService()
