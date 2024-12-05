import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, IntegrityError

from tinymce import models as tinymce_models


# Create your models here.
class Theme(models.Model):
    """Represents an overall theme for your project."""
    theme_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    use_bootstrap = models.BooleanField(default=True, help_text="Use Boostrap libraries within this theme.")
    bootstrap_version = models.CharField(max_length=100, default="5.3", help_text="The version of Bootstrap to use for this theme.", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.user:  # Check if object is new
            self.user = self.request.user  # Replace 1 with the desired user ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.theme_name


class ColorScheme(models.Model):
    """Defines color options for primary, secondary, background, text, etc."""
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="colorschemes")
    primary_color = models.CharField(max_length=50)
    secondary_color = models.CharField(max_length=50)
    background_color = models.CharField(max_length=50)
    text_color = models.CharField(max_length=50)
    accent_color = models.CharField(max_length=50)


class Typography(models.Model):
    """Sets fonts and sizes for different text elements."""
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="typographys")
    font_family = models.CharField(max_length=50)
    base_font_size = models.CharField(max_length=50)
    heading_font_size = models.JSONField()


class Layout(models.Model):
    """Controls the structural elements."""
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="layouts")
    header = models.CharField(max_length=50, blank=True, null=True, default="default_header.html")
    footer = models.CharField(max_length=50, blank=True, null=True, default="default_footer.html")
    container_width = models.CharField(max_length=50, blank=True, null=True, help_text="The width of the layout containers (e.g., '1200px' or '80%'.")
    padding = models.CharField(max_length=50, blank=True, null=True)
    margin = models.CharField(max_length=50, blank=True, null=True)
    border_radius = models.CharField(max_length=50, blank=True, null=True)


class AnimationSettings(models.Model):
    """Optional animations for transitions and interactions."""
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="animationsettings")
    animation_type = models.CharField(max_length=50, blank=True, null=True, help_text="The animation type to use. (e.g., 'fade', 'slide'")
    duration = models.CharField(max_length=50, blank=True, null=True, help_text="The duration (in seconds) of the animation.")
    delay = models.CharField(max_length=50, blank=True, null=True, help_text="The delay (in seconds) of the animation.")


class CustomCSS(models.Model):
    """Allows additional styling overrides."""
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="customcss")
    custom_css = models.TextField(blank=True, null=True)


class CSSProperty(models.Model):
    stylesheet = models.ForeignKey('CustomCSS', on_delete=models.CASCADE, related_name="cssproperties")
    selector = models.CharField(max_length=50, blank=True, null=True)
    properties = models.JSONField()

    def __str__(self):
        properties_str = "; ".join([f"{k}: {v}" for k, v in self.properties.items()])
        return f"{self.selector} {{ {properties_str}; }}"


class Header(models.Model):
    @staticmethod
    def get_template_path(path=None):
        default_path = "themebuilder/layout/headers/custom"
        path = path if path is not None else default_path
        return path

    name = models.CharField(max_length=50)
    template = models.FileField(upload_to=get_template_path())

    def __init__(self, *args, **kwargs):
        path = kwargs.pop("path", None)
        super().__init__(*args, **kwargs)
        if path:
            self.template.__setattr__('upload_to', self.get_template_path(path=path))

    def __str__(self):
        return self.name


class Footer(models.Model):
    @staticmethod
    def get_template_path(path=None):
        default_path = "themebuilder/layout/footers/custom"
        path = path if path is not None else default_path
        return path

    name = models.CharField(max_length=50)
    template = models.FileField(upload_to=get_template_path())

    def __init__(self, *args, **kwargs):
        path = kwargs.pop("path", None)
        super().__init__(*args, **kwargs)
        if path:
            self.template.__setattr__('upload_to', self.get_template_path(path=path))

    def __str__(self):
        return self.name
