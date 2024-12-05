from django.contrib import admin

from .models.models import *


# Register your models here.
class ColorSchemeInline(admin.StackedInline):
    model = ColorScheme
    extra = 1


class TypographyInline(admin.StackedInline):
    model = Typography
    extra = 1


class LayoutInline(admin.StackedInline):
    model = Layout
    extra = 1


class AnimationSettingsInline(admin.StackedInline):
    model = AnimationSettings
    extra = 1


class CustomCSSInline(admin.StackedInline):
    model = CustomCSS
    extra = 1


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    inlines = [ColorSchemeInline, TypographyInline, LayoutInline, AnimationSettingsInline, CustomCSSInline]
    readonly_fields = ('created', 'modified', "user")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "theme_name",
                    "description",
                    ("use_bootstrap", "bootstrap_version"),
                    "is_active",
                    "created",
                    "modified",
                    "user",
                ]
            }
        ),
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
