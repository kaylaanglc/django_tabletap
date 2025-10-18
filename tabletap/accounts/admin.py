from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Subscription


# Custom admin site restricted to superusers
class SuperuserOnlyAdminSite(AdminSite):
    site_header = "TableTap Admin"
    site_title = "TableTap Admin Portal"
    index_title = "Welcome to the TableTap Admin"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


# Instantiate custom admin site
admin_site = SuperuserOnlyAdminSite(name='superuseradmin')


# Get the custom or default User model
User = get_user_model()
admin_site.register(User)


# Custom admin actions
@admin.action(description="Mark selected subscriptions as Active")
def mark_as_active(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description="Archive selected subscriptions")
def mark_as_archived(modeladmin, request, queryset):
    queryset.update(active=False)


# Subscription admin
@admin.register(Subscription, site=admin_site)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "active", "created_at", "updated_at")
    search_fields = ("user__email",)
    list_filter = ("active",)
    actions = [mark_as_active, mark_as_archived]
