import json
import os

import django.db.utils
from django.apps import apps
from django.conf import settings

from themebuilder.models.models import Theme, ColorScheme, Typography, Layout, AnimationSettings, CustomCSS


def get_theme_data(instance):
    """Takes an instance and creates a dictionary that maps to the form."""
    colorscheme = instance.colorschemes.first()
    typography = instance.typographys.first()
    layout = instance.layouts.first()
    animationsettings = instance.animationsettings.first()
    customcss = instance.customcss.first()
    data = {
        'theme_name': instance.theme_name if instance.theme_name else None,
        'description': instance.description if instance.description else None,
        'use_bootstrap': instance.use_bootstrap if instance.use_bootstrap else None,
        'is_active': instance.is_active if instance.is_active else None,
        'primary_color': colorscheme.primary_color if colorscheme.primary_color else None,
        'secondary_color': colorscheme.secondary_color if colorscheme.secondary_color else None,
        'background_color': colorscheme.background_color if colorscheme.background_color else None,
        'text_color': colorscheme.text_color if colorscheme.text_color else None,
        'accent_color': colorscheme.accent_color if colorscheme.accent_color else None,
        'font_family': typography.font_family if typography.font_family else None,
        'base_font_size': typography.base_font_size if typography.base_font_size else None,
        'header': layout.header if layout.header else None,
        'footer': layout.footer if layout.footer else None,
        'container_width': layout.container_width if layout.container_width else None,
        'padding': layout.padding if layout.padding else None,
        'margin': layout.margin if layout.margin else None,
        'border_radius': layout.border_radius if layout.border_radius else None,
        'animation_type': animationsettings.animation_type if animationsettings.animation_type else None,
        'duration': animationsettings.duration if animationsettings.duration else None,
        'delay': animationsettings.delay if animationsettings.delay else None,
        'custom_css': customcss.custom_css if customcss else None,
    }
    if typography.heading_font_size is not None:
        data.update(typography.heading_font_size)

    return data


def save_new_theme(fields, current_user):
    try:
        # creating the theme instance
        theme_fields = {
            "theme_name": fields["theme_name"] if fields["theme_name"] else None,
            "description": fields["description"] if fields["description"] else None,
            "use_bootstrap": fields["use_bootstrap"] if fields["use_bootstrap"] else None,
            "bootstrap_version": fields["bootstrap_version"] if fields["bootstrap_version"] else None,
            "is_active": fields["is_active"] if fields["is_active"] else None,
            "user": current_user,
        }
        theme = Theme.objects.create(**theme_fields)
        theme.save()

        # saving colorscheme
        colorscheme_fields = {
            "theme": theme,
            "primary_color": fields["primary_color"] if fields["primary_color"] else "#333333",
            "secondary_color": fields["secondary_color"] if fields["secondary_color"] else "#555555",
            "background_color": fields["background_color"] if fields["background_color"] else "#f0f0f0",
            "text_color": fields["text_color"] if fields["text_color"] else "#000000",
            "accent_color": fields["accent_color"] if fields["accent_color"] else "#ff5722",
        }
        colorscheme = ColorScheme.objects.create(**colorscheme_fields)
        colorscheme.save()

        # saving typography
        heading_font_sizes = {
            "h1_size": fields["h1_size"] if fields["h1_size"] else "32px",
            "h2_size": fields["h2_size"] if fields["h2_size"] else "28px",
            "h3_size": fields["h3_size"] if fields["h3_size"] else "24px",
            "h4_size": fields["h4_size"] if fields["h4_size"] else "20px",
            "h5_size": fields["h5_size"] if fields["h5_size"] else "18px",
            "h6_size": fields["h6_size"] if fields["h6_size"] else "16px",
        }
        typography_fields = {
            "theme": theme,
            "font_family": fields["font_family"] if fields["font_family"] else "Arial, sans-serif",
            "base_font_size": fields["base_font_size"] if fields["base_font_size"] else "16px",
            "heading_font_size": heading_font_sizes,
        }
        typography = Typography.objects.create(**typography_fields)
        typography.save()

        # saving layout
        layout_fields = {
            "theme": theme,
            "header": fields["header"] if fields["header"] else None,
            "footer": fields["footer"] if fields["footer"] else None,
            "container_width": fields["container_width"] if fields["container_width"] else "80%",
            "padding": fields["padding"] if fields["padding"] else "16px",
            "margin": fields["margin"] if fields["margin"] else "16px",
            "border_radius": fields["border_radius"] if fields["border_radius"] else "4px",
        }
        layout = Layout.objects.create(**layout_fields)
        layout.save()

        # saving animationsettings
        animationsettings_fields = {
            "theme": theme,
            "animation_type": fields["animation_type"] if fields["animation_type"] else "fade",
            "duration": fields["duration"] if fields["duration"] else 0.5,
            "delay": fields["delay"] if fields["delay"] else 0,
        }
        animationsettings = AnimationSettings.objects.create(**animationsettings_fields)
        animationsettings.save()

        # saving customcss
        customcss_fields = {
            "theme": theme,
            "custom_css": fields["custom_css"] if fields["custom_css"] else None,
        }
        customcss = CustomCSS.objects.create(**customcss_fields)
        customcss.save()

        return theme
    except django.db.utils.Error:
        return None


def save_data_to_model(instance, data):
    try:
        for k, v in data.items():
            setattr(instance, k, v)
        return instance
    except django.db.utils.IntegrityError:
        return False


def save_existing_theme(fields, instance):
    try:
        # creating the theme instance
        theme_fields = {
            "theme_name": fields["theme_name"] if fields["theme_name"] else None,
            "description": fields["description"] if fields["description"] else None,
            "use_bootstrap": fields["use_bootstrap"] if fields["use_bootstrap"] else None,
            "bootstrap_version": fields["bootstrap_version"] if fields["bootstrap_version"] else None,
            "is_active": fields["is_active"] if fields["is_active"] else None,
        }
        theme = save_data_to_model(instance, theme_fields)
        theme.save()

        # saving colorscheme
        colorscheme_fields = {
            "theme": theme,
            "primary_color": fields["primary_color"],
            "secondary_color": fields["secondary_color"],
            "background_color": fields["background_color"],
            "text_color": fields["text_color"],
            "accent_color": fields["accent_color"],
        }
        colorscheme, created = ColorScheme.objects.get_or_create(pk=instance.colorschemes.first().pk, **colorscheme_fields)
        if not created:
            save_data_to_model(colorscheme, colorscheme_fields)
        colorscheme.save()

        # saving typography
        heading_font_sizes = {
            "h1_size": fields["h1_size"],
            "h2_size": fields["h2_size"],
            "h3_size": fields["h3_size"],
            "h4_size": fields["h4_size"],
            "h5_size": fields["h5_size"],
            "h6_size": fields["h6_size"],
        }
        typography_fields = {
            "theme": theme,
            "font_family": fields["font_family"],
            "base_font_size": fields["base_font_size"],
            "heading_font_size": heading_font_sizes,
        }
        typography, created = Typography.objects.get_or_create(pk=instance.typographys.first().pk, **typography_fields)
        if not created:
            save_data_to_model(typography, typography_fields)
        typography.save()

        # saving layout
        def set_template_path(template_type, template, default=False):
            """sets the absolute template path"""
            templates_dir = "themebuilder\\layout"
            if "default_" in template:
                default = True

            if template.isdigit():
                return template
            else:
                if default:
                    return os.path.join(templates_dir, f"{template_type}s", template)
                else:
                    return os.path.join(templates_dir, f"{template_type}s", "custom", template)

        layout_fields = {
            "theme": theme,
            "header": set_template_path("header", fields["header"]),
            "footer": set_template_path("footer", fields["footer"]),
            "container_width": fields["container_width"],
            "padding": fields["padding"],
            "margin": fields["margin"],
            "border_radius": fields["border_radius"],
        }
        layout = instance.layouts.first()
        if layout:
            save_data_to_model(layout, layout_fields)
        else:
            Layout.objects.create(**layout_fields)
        layout.save()

        # saving animationsettings
        animationsettings_fields = {
            "theme": theme,
            "animation_type": fields["animation_type"],
            "duration": fields["duration"],
            "delay": fields["delay"],
        }
        animationsettings, created = AnimationSettings.objects.get_or_create(pk=instance.animationsettings.first().pk, **animationsettings_fields)
        if not created:
            save_data_to_model(animationsettings, animationsettings_fields)
        animationsettings.save()

        # saving customcss
        customcss_fields = {
            "theme": theme,
            "custom_css": fields["custom_css"],
        }
        customcss = instance.customcss.first()
        if customcss:
            save_data_to_model(customcss, customcss_fields)
        else:
            CustomCSS.objects.create(**customcss_fields)
        customcss.save()
        return theme
    except django.db.utils.Error as e:
        print(e)
        return instance


def get_template_choices(template_type):
    model = apps.get_model("themebuilder", template_type)
    templates_dir = os.path.join(settings.BASE_DIR, "themebuilder", "templates", "themebuilder", "layout", template_type + "s")
    templates = os.listdir(templates_dir)
    custom_templates = model.objects.all()
    choices = [(template.pk, template.name) for template in custom_templates]
    for template in templates:
        if os.path.isfile(os.path.join(templates_dir, template)):
            choices.append((template, template.strip('.html')))
    return choices


def get_template(instance, template_type):
    layout = instance.layouts.first()
    template = layout.__getattribute__(template_type)
    model = apps.get_model("themebuilder", template_type)

    if template.isdigit():
        template_instance = model.objects.get(pk=int(template))
        return template_instance.template.path
    else:
        return template
