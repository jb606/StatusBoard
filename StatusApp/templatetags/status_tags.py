from django import template
from django.utils.html import format_html
from django.contrib.auth import get_user_model

register = template.Library()


@register.simple_tag
def status_modal_target():
    html = """
<div id="set_status" class="modal fade" role="dialog">
   <div id="set_status_dialog" class="modal-dialog" role="document" hx-target="modal-dialog"></div>
</div>
"""
    return format_html(html)


@register.filter(name="has_group")
def has_group(user, group_name):
    if not user.is_authenticated:
        print("Not auth")
        return False
    print(user.groups)
    a = user.groups
    print(a)
    return user.groups.filter(name__iexact=group_name).exists()


@register.filter(name="is_status_admin")
def is_status_admin(user):
    security_group = "StatusApp_GroupAdmins"
    if user.user.groups.filter(name=security_group).exists():
        return True
    return False
