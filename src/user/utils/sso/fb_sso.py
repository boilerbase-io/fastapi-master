from typing import Tuple

import requests

from src.config import Config
from src.user.utils.sso import BaseSSO


class FacebookSSO(BaseSSO):
    def __init__(self):
        self.scopes = ["email", "public_profile"]
        # self.base_auth_url = "https://www.facebook.com/v18.0/dialog/oauth"
        self.base_auth_url = "https://www.facebook.com/dialog/oauth"
        self.token_url = "https://graph.facebook.com/oauth/access_token"
        self.user_info_url = (
            "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
        )

    def get_authorization_url(self) -> str:
        return requests.get(
            url=self.base_auth_url,
            params={
                "client_id": Config.FB_CLIENT_ID,
                "redirect_uri": Config.FB_AUTH_REDIRECT_URI,
                "scope": "+".join(self.scopes),
            },
        ).url

    def get_access_token(self, code) -> str:
        response = requests.get(
            self.token_url,
            params={
                "client_id": Config.FB_CLIENT_ID,
                "redirect_uri": Config.FB_AUTH_REDIRECT_URI,
                "client_secret": Config.FB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        return response.json()["access_token"]

    def get_user_info(self, access_token) -> Tuple[str, str, str, str]:
        response = requests.get(
            self.user_info_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        user_info = response.json()
        email = user_info["email"]
        first_name = user_info["name"].split(" ")[0]
        last_name = user_info["name"].split(" ")[-1]
        picture_url = user_info.get("picture", {}).get("data", {}).get("url")
        return (
            email,
            first_name,
            last_name,
            picture_url,
        )
