from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from django_keycloak.urls import KEYCLOAK_BASE_PATH, KEYCLOAK_ADMIN_USER_PAGE

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "is_staff",
        "is_superuser",
    )
    list_display_links('username', )
    fields = [
        "username",
        "keycloak_link",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        'user_permissions',
        'groups',
    ]
    readonly_fields = ["keycloak_link", "email", "first_name", "last_name"]

    search_fields = ["username", "email"]

    def keycloak_link(self, obj):
        config = settings.KEYCLOAK_CONFIG
        label = obj.username
        base_path = config.get("BASE_PATH", KEYCLOAK_BASE_PATH)
        host = f"{config.get('SERVER_URL')}{base_path}"
        link = KEYCLOAK_ADMIN_USER_PAGE.format(
            host=host, realm=config.get("REALM"), id=obj.keycloak_id
        )
        return format_html(
            '<a href="{link}" target="_blank">{label}</a>', link=link, label=label
        )

    keycloak_link.short_description = _("keycloak link")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
