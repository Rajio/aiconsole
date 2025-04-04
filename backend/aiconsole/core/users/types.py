from typing import Optional

from pydantic import BaseModel, model_validator

DEFAULT_USERNAME = "user"


class PartialUserProfile(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    gravatar: Optional[bool] = None


class UserProfile(BaseModel):
    """User profile data model"""

    id: str
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    gravatar: bool = False

    @model_validator(mode="after")
    def set_default_username(self):
        if not self.username:
            email = self.email
            if email:
                self.username = email.split("@")[0]
            else:
                self.username = DEFAULT_USERNAME
        return self
