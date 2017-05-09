from django.conf.urls import url

from ..views.user import (SSOAPI, AvatarUploadAPI, TwoFactorAuthAPI,
                          UserNameAPI, UserInfoAPI, UserProfileAPI)

urlpatterns = [
    url(r"^username/?$", UserNameAPI.as_view(), name="user_name_api"),
    url(r"^user/(?P<username>\w+)/?$", UserInfoAPI.as_view(), name="user_info_api"),
    url(r"^profile/?$", UserProfileAPI.as_view(), name="user_profile_api"),
    url(r"^avatar/upload/?$", AvatarUploadAPI.as_view(), name="avatar_upload_api"),
    url(r"^sso/?$", SSOAPI.as_view(), name="sso_api"),
    url(r"^two_factor_auth/?$", TwoFactorAuthAPI.as_view(), name="two_factor_auth_api")
]
