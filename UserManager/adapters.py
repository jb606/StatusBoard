from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as SystemGroup
from django.conf import settings
from StatusApp.models import UserStatus
from StatusApp.models import Group as StatusGroup
#user = get_user_model()
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user_info = sociallogin.account.extra_data.get('userinfo', {})
        user_roles = user_info.get('roles', [])
        if settings.OIDC_SITE_ADMIN_ROLE in user_roles:
            user.is_superuser = True
            user.is_staff = True
        elif settings.OIDC_STAFF_ROLE in user_roles:
            user.is_staff = True
        elif settings.OIDC_GROUPADM_ROLE in user_roles:
                group = SystemGroup.objects.get("StatusApp_GroupAdmins")
                user.groups.add(group)
                user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        print("Save user called")
        user.save()
        return user

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user_info = sociallogin.account.extra_data.get('userinfo', {})
        
        user_roles = user_info.get('roles', [])
        
        if settings.OIDC_SITE_ADMIN_ROLE in user_roles:
            user.is_superuser = True
            user.is_staff = True
        elif settings.OIDC_STAFF_ROLE in user_roles:
            user.is_staff = True
        elif settings.OIDC_GROUPADM_ROLE in user_roles:
                user.is_staff = True
        else:
            user.is_staff = False
            user.is_superuser = False

        return user

    def pre_social_login(self, request, sociallogin):
        if sociallogin:
            user = sociallogin.user
            user_info = sociallogin.account.extra_data.get('userinfo', {})
            user_roles = user_info.get('roles', [])
            group_membership = user_info.get('memberof', [] )
            if settings.OIDC_SITE_ADMIN_ROLE in user_roles:
                user.is_superuser = True
                user.is_staff = True
            elif settings.OIDC_STAFF_ROLE in user_roles:
                user.is_staff = True
            elif settings.OIDC_GROUPADM_ROLE in user_roles:
                group = SystemGroup.objects.get(name="StatusApp_GroupAdmins")
                user.groups.add(group)
                print(group)
                user.is_staff = True
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
            user_status = UserStatus.objects.get(user=user)
            sso_groups = StatusGroup.objects.filter(external_sync=True).filter(name__in=group_membership)
            user_status_groups = user_status.member_of.filter(external_sync=True)
            for g in sso_groups:
                if g not in user_status_groups:
                    g.members.add(user_status)
                    print(f"Add {g} to {user}")

            for g in user_status_groups:
                if g not in sso_groups:
                    g.members.remove(user_status)
                    print(f"Remove {g} from {user}")

            #print(sso_groups)
            #print()